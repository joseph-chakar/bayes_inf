# What's included in this repo

This repo introduces the Bayesian framework from a practical, hands-on perspective. Instead of treating parameters as fixed values, the goal is to view them as variables described by probability distributions. In PV research, this shift is essential: many problems are inherently multi-solution, and classical deterministic approaches that search for a single "best fit" can be misleading. A more in-depth discussion of these ideas and their implications for PV research is available in my PhD dissertation (https://theses.fr/2024IPPAX120).

### 📘 Introductory material

* A conceptual introduction to the probabilistic Bayesian framework (see below).

### ⚙️ Example notebook

* `ideal_diode_example.ipynb`

  Benchmarks my very first Bayesian parameter estimation implementation against the pioneering code from MIT's PV-Lab, demonstrating how optimized data structures can cut computing time from hours to minutes/seconds.

### 📄 Related publications and applications

Published studies where I applied more advanced versions of this code - with some predictions validated experimentally - in collaboration with national and international PV research groups and companies.

* **Material vs. Interface Effects on Performance in Perovskite Solar Cells** (https://doi.org/10.1021/acsenergylett.5c02406)

   Bayesian inference + drift-diffusion modeling reveals that the passivation layer at the interface between the perovskite and electron transport layer boosts solar cell efficiency mostly by reducing defects in the perovskite bulk, as evidenced by ToF-SIMS measurements.

* **Indoor vs. Outdoor Aging of Novel Solar Cell Technologies** (https://doi.org/10.1002/solr.202500716)

  Bayesian inference + drift-diffusion modeling provides the first quantitative link between accelerated indoor testing and outdoor aging in perovskite solar cells using standard current–voltage curves, showing shared degradation mechanisms and new ones activated by elevated stress levels.

* **Performance Analysis of PV Systems** (https://doi.org/10.1016/j.solener.2024.112595)

  Bayesian inference + circuit modeling to obtain confidence intervals for degradation rates estimated from information-limited production data, with prediction uncertainty quantified for repowering applications and indetified current losses accurately traced to their sources.

# Bayesian Inference

Bayesian inference is based on Bayes' Theorem, which can be derived from the simple definition of conditional probability:

$$P(A|B) = \frac{P(A,B)}{P(B)} = \frac{P(A) P(B|A)}{P(B)}$$

It describes the probability of event A occurring given that event B is true. $P(A|B)$ is also called the _posterior_ probability (i.e. our updated knowledge of A, after observing B), and it is equal to the product of the _prior_ probability $P(A)$ (i.e. our prior knowledge of A, before knowing anything about B) and the _likelihood_ $P(B|A)$ (i.e. how likely A is, based only on the evidence provided by B), divided by the marginal probability $P(B)$ (i.e. the chances of B happening).

The coin toss example given by Bayes' Group is an excellent way to visualize this concept. Say we have a coin and want to know the probability of getting Heads. This can’t be done with deterministic approaches that return a single “best-fit” value, because multiple outcomes are plausible.

Common sense tells us that if the coin is fair, we have a 50/50 chance of getting Heads or Tails (prior distribution). If we toss the coin twice and land on Heads each time, the evidence (likelihood) we have so far suggests that we are more likely to get Heads than Tails (posterior distribution). 

<p align="center">
  <img src="https://vitalflux.com/wp-content/uploads/2020/09/Screenshot-2020-09-13-at-9.29.35-AM-300x202.png">
</p>

However, suppose we keep tossing the coin 1000 times and end up with 489 Tails and 511 Heads. This fresh evidence allows us to adjust our posterior, indicating that the coin aligns with our initial expectations and is likely to be fair.

Bayes' theorem provides a method of calculating the degree of (un)certainty, and has many applications. In PV for example, we can use it to fit solar cell parameters $&theta;$ on some observed data $d$ (e.g. current-voltage data), accounting for the fact that multiple parameter combinations can reproduce the measured data:

$$P(&theta;|d) = \frac{P(&theta;) P(d|&theta;)}{P(d)}$$

Here, the prior $P(&theta;)$ reflects our pre-existing knowledge of the parameters (e.g. from physics/chemistry, previous experience, or the literature). The likelihood $P(d|&theta;)$ is the probability of observing the given (experimental) data for each hypothesized (often simulated) combination of these parameters. As can be noticed, Bayesian inference requires us to have some physical knowledge and model(s) to generate enough hypotheses and compute the likelihood, which can be computationally expensive. $P(d)$ is simply the sum of $P(&theta;)*P(d|&theta;)$ over all the possible hypotheses. This normalization constant prevents the certainty in any given hypothesis from being related to the likelihood of that particular hypothesis only, by dampening it with the likelihoods of all the other hypotheses.

**References:**

- http://deepbayes.ru/

- https://en.wikipedia.org/wiki/Bayes%27_theorem
