# Bayesian Inference

Bayesian inference is based on Bayes' Theorem, which can be derived from the simple definition of conditional probability:

$$P(A|B) = \frac{P(A,B)}{P(B)} = \frac{P(A) P(B|A)}{P(B)}$$

It describes the probability of event A occurring given that event B is true. $P(A|B)$ is also called the posterior probability _(i.e. our updated knowledge of A, after observing B)_, and it is equal to the product of the prior (or marginal) probability $P(A)$ _(i.e. our prior knowledge of A, before knowing anything about B)_ and the likelihood $P(B|A)$ _(i.e. how likely A is, based only on the evidence provided by B)_, divided by the marginal probability $P(B)$ _(i.e. the chances of B happening)_.

The coin toss example given by Bayes' Group is an excellent way to visualize this concept. We have a coin that we think is fair (prior = 50/50 chance of getting Heads or Tails), but we wish to test this coin to determine the actual probability of getting Heads (posterior). Say we toss the coin twice and land on Heads each time. The evidence we now have suggests that we are more likely to get Heads than Tails. 

<p align="center">
  <img src="https://vitalflux.com/wp-content/uploads/2020/09/Screenshot-2020-09-13-at-9.29.35-AM-300x202.png">
</p>

However, suppose we keep tossing the coin 1000 times and end up with 489 Tails and 511 Heads. This fresh evidence allows us to adjust our posterior, indicating that the coin aligns with our initial expectations and is likely to be fair.

Bayes' theorem provides a method of calculating the degree of (un)certainty, and has many applications. In PV for example, we can use it to fit solar cell parameters $&theta;$ on some observed data $d$ (e.g. current-voltage data):

$$P(&theta;|d) = \frac{P(&theta;) P(d|&theta;)}{P(d)}$$

Here, the prior $P(&theta;)$ reflects our pre-existing knowledge of the parameters (from physics or chemistry). The likelihood $P(d|&theta;)$ is the probability of obtaining the observed (experimental) data for hypothesized (and often simulated) combinations of these parameters. As can be noticed, Bayesian inference requires us to have some physical knowledge and model(s) to generate enough hypotheses and compute the likelihood, which can be computationally expensive. $P(d)$ is simply the sum of $P(&theta;)*P(d|&theta;)$ over all the possible hypotheses. This normalization constant prevents the certainty in any given hypothesis from being related to the likelihood of that particular hypothesis only, by dampening it with the likelihoods of all the other hypotheses.

In the `ideal_diode_example.ipynb` notebook, I show my implementation of Bayesian parameter inference and validate the results using this benchmark code from MIT’s PV-lab: https://github.com/PV-Lab/bayesim/blob/master/examples/diode/ideal_diode.ipynb

You can also check out my latest pre-print (article still under review) included in this repo to see how we can use Bayesian inference to perform advanced remote PV degradation analysis: https://dx.doi.org/10.2139/ssrn.4593263

Some features are still missing from this work in progress, but I just wanted to demonstrate a draft version that can yield (almost) the exact same results of this popular version in just a fraction of the time.

**References:**

- http://deepbayes.ru/

- https://en.wikipedia.org/wiki/Bayes%27_theorem
