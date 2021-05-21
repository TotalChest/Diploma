import numpy as np
import random
from pathlib import Path
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Dense,
    Dropout,
    Conv2D,
    MaxPooling2D,
    Activation,
    Flatten
)
from tensorflow.keras.optimizers import Adam
from collections import deque

from stem.core.view_utils import view_processor
from stem.core.utils import get_downscale_ratio


DISCOUNT = 0.9
MINIBATCH_SIZE = 8
UPDATE_TARGET_EVERY = 40

IMAGE_SIZE = (180, 320, 3)

WEIGHTS_PATH = 'DQN_weights/last'

class DQNAgent:
    def __init__(self, device_width, device_height,
                 device_back_button_bounds):

        self.screen_dim = (device_width, device_height)
        self.back_button_bounds = device_back_button_bounds
        self.downscale_ratio = get_downscale_ratio(self.screen_dim)

        self.state = None
        self.last_state = None

        self.replay_memory = {}
        self.target_update_counter = 0

        # Main model
        self.model = self.create_model()
        if Path(WEIGHTS_PATH).with_suffix('.index').exists():
            self.model.load_weights(WEIGHTS_PATH)

        # Target network
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

    def create_model(self):
        model = Sequential()

        model.add(Conv2D(10, (5, 5), input_shape=IMAGE_SIZE))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        model.add(Conv2D(8, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        model.add(Flatten())
        model.add(Dense(64, activation='sigmoid'))

        model.add(Dense(1, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=0.001),
                      metrics=['mse'])
        return model

    def update_replay_memory(self, event_view_trees, reward, current_state):
        model_input = self._prepare_input(event_view_trees,
                                          state=self.last_state)

        # Replace if already exists model_input
        self.replay_memory[model_input.tobytes()] = (model_input,
                                                     reward,
                                                     self.state,
                                                     current_state)

    def update_state(self, state_view_tree):
        self.last_state = self.state
        self.state = view_processor.process(state_view_tree,
                                            self.screen_dim,
                                            self.back_button_bounds)[:, :, :2]

    def predict(self, possible_events, *, target_model=False):
        model_input = []
        for event in possible_events:
            model_input.append(self._prepare_input(event.get_views(),
                                                   self.state))

        model = self.target_model if target_model else self.model
        q_values = self.model.predict(
            np.array(model_input).reshape(-1, *IMAGE_SIZE)
        ).ravel()

        return q_values

    def _prepare_input(self, event_view_trees, state):
        event_array = np.zeros(IMAGE_SIZE[:2])
        if event_view_trees:
            event_bounds = event_view_trees[0].bounds
        else:
            # key BACK
            event_bounds = self.back_button_bounds

        downscale_bounds = [
            int(event_bounds[0] * self.downscale_ratio[0]),
            int(event_bounds[1] * self.downscale_ratio[1]),
            int(event_bounds[2] * self.downscale_ratio[0]),
            int(event_bounds[3] * self.downscale_ratio[1])
        ]

        # FIXME: invalid back_button_bounds
        if not event_view_trees:
            downscale_bounds = [0, 300, 180, 320]

        event_array[
            downscale_bounds[0]:downscale_bounds[2],
            downscale_bounds[1]:downscale_bounds[3]
        ] = 1

        state_with_event = np.concatenate(
            [state, event_array[:, :, None]], axis=2
        )

        return state_with_event

    def train(self):

        minibatch = random.sample(list(self.replay_memory.values()),
                                  min(len(self.replay_memory),
                                  MINIBATCH_SIZE))

        X = []
        y = []
        saved_current_state = self.state
        for current_input, reward, new_state, new_view_state in minibatch:
            possible_events = new_view_state.get_possible_input()
            if not possible_events:
                continue
            self.state = new_state
            future_qs_list = self.predict(possible_events, target_model=True)

            max_future_q = np.max(future_qs_list)
            new_q = reward + DISCOUNT * max_future_q

            X.append(current_input)
            y.append(new_q)

        self.state = saved_current_state

        self.model.fit(np.array(X), np.array(y),
                       batch_size=MINIBATCH_SIZE, verbose=0, shuffle=False)

        self.target_update_counter += 1
        if self.target_update_counter > UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0
