# 05 Model-Based Agents

**Course:** AI-Atlas: Foundations of AI $\mid$ **Chapter:** Intelligent Agents
**Topic:** Model-Based Agents (MBAs)

---

## 5.1 Introduction to Model-Based Agents

Model-Based Agents (MBAs) represent a significant step up from simpler agents like Simple Reflex Agents. While reflex agents only consider the *current percept* to decide an action, Model-Based Agents maintain an internal representation of the world, often called the **"internal state"** or **"world model."**

This internal model allows the agent to reason about the effects of its actions, anticipate future states, and make informed decisions even when the current percept is incomplete or ambiguous.

### 5.1.1 The Need for a Model

In partially observable environments (the norm in the real world), the current percept alone is insufficient to determine the correct action.

**Example:**
Imagine an autonomous vacuum cleaner. If its current sensor reading is "bumped into an object," a Simple Reflex Agent might just execute "turn left." However, if the agent *knows* (via its model) that it is currently in a corner, turning left might immediately lead to another collision. A Model-Based Agent uses its history of percepts and actions to build an understanding of the environment's structure and its own location (its state).

## 5.2 Definition and Structure

A Model-Based Agent requires two crucial pieces of knowledge beyond the simple reflex mapping:

1.  **How the world evolves independently of the agent's actions.** (The dynamics of the environment.)
2.  **How the agent's actions affect the world.** (The agent's capabilities.)

### Formal Definition: Model-Based Agent

A **Model-Based Agent (MBA)** is an intelligent agent that maintains an internal state representation, often called the **World Model ($\mathcal{M}$)**, which is updated based on the sequence of percepts and actions. The agent uses this model, along with a set of goals or utility functions, to select actions that lead to desired future states.

### Key Components of an MBA

The MBA architecture includes three primary internal knowledge structures:

1.  **The State:** What the world is like *now*. This is the agent's internal belief state ($S_t$), often reconstructed from the history of percepts and actions.
2.  **The Model (Transition Model):** How the world changes. This model predicts the next state ($S_{t+1}$) given the current state ($S_t$) and the action ($A_t$).
    $$
    S_{t+1} \approx P(S_{t+1} | S_t, A_t)
    $$
3.  **The Sensor Model (Percept Model):** How the world appears. This model describes the relationship between the actual state and the percept received ($P_t$).
    $$
    P_t \approx P(P_t | S_t)
    $$

## 5.3 State Estimation and World Dynamics

A core function of the MBA is **State Estimation** (or **State Tracking**). Since the agent cannot directly observe the full state, it must combine its current belief state with the new percept to form an updated belief state.

### 5.3.1 Updating the Internal State

The agent uses its existing state, the action it just took, and the new percept to update its belief about the environment.

Let $S_{t-1}$ be the belief state at time $t-1$, $A_{t-1}$ the action taken, and $P_t$ the new percept. The new state $S_t$ is estimated:

$$
S_t = \text{UPDATE\_STATE}(S_{t-1}, A_{t-1}, P_t)
$$

In probabilistic settings (common in robotics and modern AI), this is often handled by **Bayesian Filtering** (e.g., Kalman Filters or Particle Filters) where $S_t$ is a probability distribution over possible states.

$$
P(S_t | P_{1:t}, A_{1:t-1}) \propto P(P_t | S_t) \sum_{S_{t-1}} P(S_t | S_{t-1}, A_{t-1}) P(S_{t-1} | P_{1:t-1}, A_{1:t-2})
$$

### 5.3.2 Planning and Prediction

Once the agent has a robust internal model ($\mathcal{M}$), it can engage in **planning**.

1.  **Prediction:** Use the transition model to forecast the likely resulting state of a sequence of actions.
2.  **Hypothetical Lookahead:** Simulate different action sequences in the internal model to evaluate their outcomes against a desired goal state or utility function.

This lookahead capability is the primary advantage of Model-Based Agents over purely reflexive ones.

## 5.4 Model-Based Agents with Goals vs. Utility

The Model-Based Agent architecture is often paired with specific decision-making strategies.

### 5.4.1 Model-Based, Goal-Based Agents

These agents use planning and search algorithms to find a sequence of actions that achieves a defined, discrete goal (e.g., reaching location X).

-   **Mechanism:** Search trees (A*, DFS, BFS).
-   **Output:** A sequence of actions leading to the goal.

### 5.4.2 Model-Based, Utility-Based Agents

These agents are designed for complex environments where maximizing a continuous measure of happiness (utility) is necessary, often in the presence of uncertainty or trade-offs.

-   **Mechanism:** Decision theory, Markov Decision Processes (MDPs), or reinforcement learning methods that rely on the model for simulated experience (e.g., Monte Carlo Tree Search (MCTS) used in AlphaGo).
-   **Output:** The action that maximizes expected utility over the long term.

## 5.5 Connections to Modern AI and LLMs

The Model-Based paradigm is central to cutting-edge AI research, particularly in areas integrating planning and learning.

### 5.5.1 Model-Based Reinforcement Learning (MBRL)

In Reinforcement Learning (RL), Model-Based approaches are distinguished from Model-Free approaches:

| Feature | Model-Free RL (e.g., DQN) | Model-Based RL (e.g., MuZero) |
| :--- | :--- | :--- |
| **Learning** | Learns the optimal policy ($\pi$) or value function ($Q$) directly. | Learns the environment model ($\mathcal{M}$) first, then uses $\mathcal{M}$ to plan. |
| **Data Efficiency** | Requires vast amounts of real-world interaction (low sample efficiency). | Highly sample efficient; can generate synthetic experience from the model. |
| **Planning** | Implicit (the learned Q-value guides the action). | Explicit (uses the model for search/lookahead). |

MBRL systems, like those developed by DeepMind (e.g., World Models, DreamerV3), use neural networks to learn the transition and sensor models, allowing agents to "dream" or simulate future trajectories purely internally before committing to a real action.

### 5.5.2 Large Language Models (LLMs) as Model-Based Agents

While often seen as purely reactive (input-output sequence generators), modern LLMs employed for planning tasks (e.g., using Chain-of-Thought or Tree-of-Thought prompting) exhibit model-based characteristics:

1.  **Internal Model:** The LLM's vast knowledge base acts as a probabilistic world model, implicitly containing rules about physics, social dynamics, and causal relationships.
2.  **Planning:** Techniques like "Self-Refine" or "ReAct" prompt the LLM to generate internal thoughts (planning steps) before generating the final action/response, effectively simulating potential outcomes within its learned model before execution.

## 5.6 Misconceptions and Common Pitfalls

### Pitfall 1: Model Error Accumulation

If the agent's internal model ($\mathcal{M}$) is slightly inaccurate, repeated use of the model for long-term planning (long lookahead) can lead to significant cumulative errors. This is the **Model Mismatch Problem.**

**Mitigation:** Continual learning and adaptation of the model, and balancing planning depth with real-world feedback (shallow planning).

### Pitfall 2: High Computational Cost

Building, maintaining, and using a detailed, accurate world model is computationally expensive. Planning (searching the state space) is often NP-hard.

**Mitigation:** Abstracting the state space (using simplified, higher-level features) and employing heuristic search or sampling methods (like MCTS) instead of exhaustive search.

### Misconception: Deterministic vs. Probabilistic Models

A common error is assuming MBAs only work with deterministic models. In reality, most sophisticated MBAs use **probabilistic models** (like MDPs) to handle the inherent uncertainty of the real world. A deterministic model is merely a special case where $P(S_{t+1} | S_t, A_t) = 1$ for one specific state.

## 5.7 Summary

Model-Based Agents represent a class of intelligent agents that maintain an internal representation of the world, allowing them to reason beyond the immediate percept. They consist of a mechanism for state estimation, a transition model, and a sensor model. By incorporating this world model, MBAs can perform sophisticated functions like prediction and explicit planning, making them robust in partially observable and complex environments. Their architectural principles are foundational to advanced AI fields like robotics and Model-Based Reinforcement Learning.

---

## Mini Quiz

1.  What is the primary knowledge structure that distinguishes a Model-Based Agent from a Simple Reflex Agent?
2.  Identify the two main internal models required by an MBA, and briefly explain the role of each.
3.  Why are Model-Based Agents generally considered more sample efficient than Model-Free Reinforcement Learning Agents?
4.  If an MBA's internal model is slightly wrong, what major practical problem can occur during long-term planning?

---

## Research Bibliography

1.  Russell, S. J., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson Education. (Chapter 2, 4, 17)
2.  Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press. (Chapter 8: Planning and Learning with Tabular Methods)
3.  Ha, D., & Schmidhuber, J. (2018). Recurrent World Models for Reinforcement Learning. *Neural Information Processing Systems (NeurIPS)*. (Introduces the foundational concept of learning a compressed model of the environment.)
4.  Silver, D., Hubert, T., Schrittwieser, J., et al. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. *Science*, 362(6419), 1140-1144. (Discusses AlphaZero, a highly successful MBRL system using MCTS.)
5.  Kaelbling, L. P., Littman, M. L., & Cassandra, A. R. (1998). Planning and acting in partially observable stochastic domains. *Artificial Intelligence*, 101(1-2), 99-134. (Foundational work on managing uncertainty in MBAs.)