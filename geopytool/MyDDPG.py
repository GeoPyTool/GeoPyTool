from ImportDependence import *
from CustomClass import *
# -*- coding: utf-8 -*-

from drl import drl

class DDPG(drl):
    """Deep Deterministic Policy Gradient Algorithms.
    """
    def __init__(self):
        super(DDPG, self).__init__()

        self.sess = K.get_session()
        self.env = gym.make('Pendulum-v0')
        self.bound = self.env.action_space.high[0]

        # update rate for target model.
        self.TAU = 0.01
        # experience replay.
        self.memory_buffer = deque(maxlen=4000)
        # discount rate for q value.
        self.gamma = 0.95
        # epsilon of action selection
        self.epsilon = 1.0
        # discount rate for epsilon.
        self.epsilon_decay = 0.995
        # min epsilon of ε-greedy.
        self.epsilon_min = 0.01

        # actor learning rate
        self.a_lr = 0.0001
        # critic learining rate
        self.c_lr = 0.001

        # ddpg model
        self.actor = self._build_actor()
        self.critic = self._build_critic()

        # target model
        self.target_actor = self._build_actor()
        self.target_actor.set_weights(self.actor.get_weights())
        self.target_critic = self._build_critic()
        self.target_critic.set_weights(self.critic.get_weights())

        # gradient function

        self.get_critic_grad = self.critic_gradient()
        self.actor_optimizer()

        if os.path.exists('model/ddpg_actor.h5') and os.path.exists('model/ddpg_critic.h5'):
            self.actor.load_weights('model/ddpg_actor.h5')
            self.critic.load_weights('model/ddpg_critic.h5')

    def _build_actor(self):
        """Actor model.
        """
        inputs = Input(shape=(3,), name='state_input')
        x = Dense(40, activation='relu')(inputs)
        x = Dense(40, activation='relu')(x)
        x = Dense(1, activation='tanh')(x)
        output = Lambda(lambda x: x * self.bound)(x)

        model = Model(inputs=inputs, outputs=output)
        model.compile(loss='mse', optimizer=Adam(lr=self.a_lr))

        return model

    def _build_critic(self):
        """Critic model.
        """
        sinput = Input(shape=(3,), name='state_input')
        ainput = Input(shape=(1,), name='action_input')
        s = Dense(40, activation='relu')(sinput)
        a = Dense(40, activation='relu')(ainput)
        x = concatenate([s, a])
        x = Dense(40, activation='relu')(x)
        output = Dense(1, activation='linear')(x)

        model = Model(inputs=[sinput, ainput], outputs=output)
        model.compile(loss='mse', optimizer=Adam(lr=self.c_lr))

        return model

    def actor_optimizer(self):
        """actor_optimizer.

        Returns:
            function, opt function for actor.
        """
        self.ainput = self.actor.input
        aoutput = self.actor.output
        trainable_weights = self.actor.trainable_weights
        self.action_gradient = tf.placeholder(tf.float32, shape=(None, 1))

        # tf.gradients will calculate dy/dx with a initial gradients for y
        # action_gradient is dq / da, so this is dq/da * da/dparams
        params_grad = tf.gradients(aoutput, trainable_weights, -self.action_gradient)
        grads = zip(params_grad, trainable_weights)
        self.opt = tf.train.AdamOptimizer(self.a_lr).apply_gradients(grads)
        self.sess.run(tf.global_variables_initializer())

    def critic_gradient(self):
        """get critic gradient function.

        Returns:
            function, gradient function for critic.
        """
        cinput = self.critic.input
        coutput = self.critic.output

        # compute the gradient of the action with q value, dq/da.
        action_grads = K.gradients(coutput, cinput[1])

        return K.function([cinput[0], cinput[1]], action_grads)

    def OU(self, x, mu=0, theta=0.15, sigma=0.2):
        """Ornstein-Uhlenbeck process.
        formula：ou = θ * (μ - x) + σ * w

        Arguments:
            x: action value.
            mu: μ, mean fo values.
            theta: θ, rate the variable reverts towards to the mean.
            sigma：σ, degree of volatility of the process.

        Returns:
            OU value
        """
        return theta * (mu - x) + sigma * np.random.randn(1)

    def get_action(self, X):
        """get actor action with ou noise.

        Arguments:
            X: state value.
        """
        action = self.actor.predict(X)[0][0]

        # add randomness to action selection for exploration
        noise = max(self.epsilon, 0) * self.OU(action)
        action = np.clip(action + noise, -self.bound, self.bound)

        return action

    def remember(self, state, action, reward, next_state, done):
        """add data to experience replay.

        Arguments:
            state: observation.
            action: action.
            reward: reward.
            next_state: next_observation.
            done: if game done.
        """
        item = (state, action, reward, next_state, done)
        self.memory_buffer.append(item)

    def update_epsilon(self):
        """update epsilon.
        """
        if self.epsilon >= self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def process_batch(self, batch):
        """process batch data.

        Arguments:
            batch: batch size.

        Returns:
            states: states.
            actions: actions.
            y: Q_value.
        """
        y = []
         # ranchom choice batch data from experience replay.
        data = random.sample(self.memory_buffer, batch)
        states = np.array([d[0] for d in data])
        actions = np.array([d[1] for d in data])
        next_states = np.array([d[3] for d in data])

        # Q_target。
        next_actions = self.target_actor.predict(next_states)
        q = self.target_critic.predict([next_states, next_actions])

        # update Q value
        for i, (_, _, reward, _, done) in enumerate(data):
            target = reward
            if not done:
                target += self.gamma * q[i][0]
            y.append(target)

        return states, actions, y

    def update_model(self, X1, X2, y):
        """update ddpg model.

        Arguments:
            states: states.
            actions: actions.
            y: Q_value.

        Returns:
            loss: critic loss.
        """
#        loss = self.critic.train_on_batch([X1, X2], y)
        loss = self.critic.fit([X1, X2], y, verbose=0)
        loss = np.mean(loss.history['loss'])

        X3 = self.actor.predict(X1)
        a_grads = np.array(self.get_critic_grad([X1, X3]))[0]
        self.sess.run(self.opt, feed_dict={
            self.ainput: X1,
            self.action_gradient: a_grads
        })

        return loss

    def update_target_model(self):
        """soft update target model.
        formula：θ​​t ← τ * θ + (1−τ) * θt, τ << 1.
        """
        critic_weights = self.critic.get_weights()
        actor_weights = self.actor.get_weights()
        critic_target_weights = self.target_critic.get_weights()
        actor_target_weights = self.target_actor.get_weights()

        for i in range(len(critic_weights)):
            critic_target_weights[i] = self.TAU * critic_weights[i] + (1 - self.TAU) * critic_target_weights[i]

        for i in range(len(actor_weights)):
            actor_target_weights[i] = self.TAU * actor_weights[i] + (1 - self.TAU) * actor_target_weights[i]

        self.target_critic.set_weights(critic_target_weights)
        self.target_actor.set_weights(actor_target_weights)

    def train(self, episode, batch):
        """training model.
        Arguments:
            episode: ganme episode.
            batch： batch size of episode.

        Returns:
            history: training history.
        """
        history = {'episode': [], 'Episode_reward': [], 'Loss': []}

        for i in range(episode):
            observation = self.env.reset()
            reward_sum = 0
            losses = []

            for j in range(200):
                # chocie action from ε-greedy.
                x = observation.reshape(-1, 3)

                # actor action
                action = self.get_action(x)
                observation, reward, done, _ = self.env.step(action)
                # add data to experience replay.
                reward_sum += reward
                self.remember(x[0], action, reward, observation, done)

                if len(self.memory_buffer) > batch:
                    X1, X2, y = self.process_batch(batch)

                    # update DDPG model
                    loss = self.update_model(X1, X2, y)
                    # update target model
                    self.update_target_model()
                    # reduce epsilon pure batch.
                    self.update_epsilon()

                    losses.append(loss)

            loss = np.mean(losses)
            history['episode'].append(i)
            history['Episode_reward'].append(reward_sum)
            history['Loss'].append(loss)

            print('Episode: {}/{} | reward: {} | loss: {:.3f}'.format(i, episode, reward_sum, loss))

        self.actor.save_weights('model/ddpg_actor.h5')
        self.critic.save_weights('model/ddpg_critic.h5')

        return history

    def play(self):
        """play game with model.
        """
        print('play...')
        observation = self.env.reset()

        reward_sum = 0
        random_episodes = 0

        while random_episodes < 10:
            self.env.render()

            x = observation.reshape(-1, 3)
            action = self.actor.predict(x)[0]
            observation, reward, done, _ = self.env.step(action)

            reward_sum += reward

            if done:
                print("Reward for this episode was: {}".format(reward_sum))
                random_episodes += 1
                reward_sum = 0
                observation = self.env.reset()

        self.env.close()


if __name__ == '__main__':
    model = DDPG()

    history = model.train(200, 128)
    model.save_history(history, 'ddpg.csv')

    model.play()

