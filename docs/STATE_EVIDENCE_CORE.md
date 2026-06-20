# ShiftLens State-Evidence Core

**Status:** first-principles mathematical specification  
**Version:** v0.2 draft  
**Scope:** public ShiftLens design foundation  
**Purpose:** define the mathematical spine for turning candidate hidden structure in time-series data into evidence-bearing state objects.

---

## 1. Root definition

A **ShiftLens state** is an evidence-region that may represent a real process condition once it survives temporal, transfer, and rejection tests.

Equivalently:

```text
candidate state = region in evidence space
validated state object = candidate state + survived evidence tests
```

ShiftLens does not treat a label, cluster ID, latent ID, or model output as a state by itself.

A state is not assigned. A state is earned by evidence survival.

---

## 2. Observed system

Let the observed time-series be:

\[
X = (x_1, x_2, ..., x_T)
\]

where each observation is:

\[
x_t \in \mathbb{R}^d
\]

For univariate data, \(d=1\). For multivariate telemetry, sensor, market, biological, industrial, or scientific data, \(d>1\).

So:

\[
X \in \mathbb{R}^{T \times d}
\]

---

## 3. Windows

A state is usually not visible from a single point. It is visible from local behaviour over time.

Define a window:

\[
W_i = (x_i, x_{i+1}, ..., x_{i+m-1})
\]

where:

\[
W_i \in \mathbb{R}^{m \times d}
\]

and:

\[
i = 1, ..., N
\]

with:

\[
N = T - m + 1
\]

The window length \(m\) is part of the lens.

---

## 4. Lens

A **lens** is the mathematical view used to expose structure in the time-series.

Define a lens:

\[
L = (\phi, d_E, \Theta, \mathcal{N})
\]

Where:

| Symbol | Meaning |
|---|---|
| \(\phi\) | feature/evidence transform |
| \(d_E\) | distance or divergence in evidence space |
| \(\Theta\) | lens parameters |
| \(\mathcal{N}\) | null or negative-control generator |

The lens maps raw windows into evidence vectors:

\[
z_i = \phi(W_i; \Theta)
\]

where:

\[
z_i \in \mathcal{E}
\]

and \(\mathcal{E}\) is the evidence space.

The lens does not define truth. The lens creates the space in which state evidence can be tested.

---

## 5. Evidence space

The transformed dataset is:

\[
Z = (z_1, z_2, ..., z_N)
\]

with:

\[
Z \in \mathbb{R}^{N \times p}
\]

where \(p\) is the number of evidence dimensions.

A state candidate lives in this evidence space.

---

## 6. Candidate state

A candidate state is a region:

\[
R_k \subseteq \mathcal{E}
\]

The hard-membership form is:

\[
S_k = \{W_i : z_i \in R_k\}
\]

The preferred form is fuzzy:

\[
\mu_k(z_i) \in [0,1]
\]

where \(\mu_k(z_i)\) is the membership strength of window \(W_i\) in candidate state \(k\).

So:

\[
S_k = \{(W_i, z_i, \mu_k(z_i))\}_{i=1}^{N}
\]

This matters because real process conditions often have soft or uncertain boundaries.

---

## 7. State prototype

The prototype of state \(k\) is its weighted evidence centre:

\[
c_k = \frac{\sum_{i=1}^{N} \mu_k(z_i) z_i}{\sum_{i=1}^{N} \mu_k(z_i)}
\]

Let effective state mass be:

\[
n_k = \sum_{i=1}^{N} \mu_k(z_i)
\]

Then:

\[
c_k = \frac{1}{n_k}\sum_{i=1}^{N} \mu_k(z_i)z_i
\]

The prototype is not ground truth. It is the current evidence summary of the candidate state.

---

## 8. Support

Support measures how much data backs the candidate:

\[
s_k = \text{support}(S_k) = \frac{n_k}{N}
\]

A candidate with too little support may be noise, an artifact, or a rare real condition. It should not be promoted without additional evidence.

Minimum support test:

\[
s_k \geq s_{min}
\]

---

## 9. Internal consistency

A state should behave like itself.

Weighted internal dispersion:

\[
\sigma_k^2 = \frac{1}{n_k}\sum_{i=1}^{N}\mu_k(z_i)d_E(z_i,c_k)^2
\]

Lower dispersion means members of the candidate state resemble each other.

Convert dispersion to a coherence score:

\[
C_k = \exp\left(-\frac{\sigma_k^2}{\tau_C}\right)
\]

where \(\tau_C\) controls strictness.

Interpretation:

- \(C_k \approx 1\): internally coherent candidate state.
- \(C_k \approx 0\): internally messy or overloaded candidate state.

---

## 10. External separation

A state should be meaningfully different from other states.

Distance between prototypes:

\[
D_{kj} = d_E(c_k,c_j)
\]

Normalized separation:

\[
\Delta_{kj} = \frac{D_{kj}}{\sqrt{\sigma_k^2 + \sigma_j^2} + \epsilon}
\]

State \(k\)'s nearest-neighbour separation is:

\[
\text{sep}(S_k) = \min_{j \neq k} \Delta_{kj}
\]

Convert to score:

\[
B_k = 1 - \exp(-\text{sep}(S_k))
\]

Low separation means the candidate may be unnecessary, overlapping, dirty, overloaded, badly bounded, or produced by a weak lens.

---

## 11. Boundary confidence

For fuzzy membership, define the membership margin:

\[
M_i^{(k)} = \mu_k(z_i) - \max_{j \neq k}\mu_j(z_i)
\]

For hard assignment:

\[
y_i = \arg\max_k \mu_k(z_i)
\]

Boundary confidence for state \(k\):

\[
Q_k = \text{median}_{i:y_i=k} M_i^{(k)}
\]

Interpretation:

- High \(Q_k\): clean boundary.
- Low \(Q_k\): ambiguous boundary.
- Near-zero or negative \(Q_k\): candidate bleeds into other states.

---

## 12. Temporal persistence

Statehood is not only geometry. A real process condition should usually have temporal structure.

Given hard assignments:

\[
y_i = \arg\max_k \mu_k(z_i)
\]

Define runs of state \(k\):

\[
\mathcal{R}_k = \{r_1, r_2, ..., r_q\}
\]

where each \(r\) is a contiguous segment with \(y_i=k\).

Mean dwell length:

\[
\bar{D}_k = \frac{1}{|\mathcal{R}_k|}\sum_{r \in \mathcal{R}_k}|r|
\]

Flicker rate:

\[
F_k = P(y_{i-1} \neq k, y_i = k, y_{i+1} \neq k)
\]

Persistence score:

\[
P_k = \text{sigmoid}\left(\frac{\bar{D}_k - \bar{D}_k^{null}}{\tau_P}\right)(1 - F_k)
\]

where \(\bar{D}_k^{null}\) comes from a null model.

Plain interpretation:

```text
Does this state form meaningful temporal runs,
or is it random flicker?
```

---

## 13. Transition structure

A real process condition may have characteristic entry and exit behaviour.

Transition count:

\[
N_{kj} = \sum_{i=1}^{N-1}\mathbf{1}[y_i=k, y_{i+1}=j]
\]

Transition probability:

\[
T_{kj} = \frac{N_{kj}}{\sum_j N_{kj}}
\]

Transition entropy:

\[
H_k^{trans} = -\sum_j T_{kj}\log(T_{kj}+\epsilon)
\]

Interpretation:

- Low transition entropy: state exits in specific ways.
- High transition entropy: state exits randomly or noisily.
- Suspicious transition structure can indicate dirty or overloaded states.

Entry-shape evidence:

\[
A_k^{-} = \{z_{i-h:i-1} : y_i = k, y_{i-1} \neq k\}
\]

Exit-shape evidence:

\[
A_k^{+} = \{z_{i+1:i+h} : y_i = k, y_{i+1} \neq k\}
\]

These ask:

```text
What does the system look like before entering this state?
What does it look like after leaving it?
```

---

## 14. Stability over time

Split the time-series into blocks:

\[
X^{(1)}, X^{(2)}, ..., X^{(B)}
\]

For each block, estimate a prototype:

\[
c_k^{(b)}
\]

State drift:

\[
G_k = \frac{1}{B}\sum_b d_E(c_k^{(b)}, c_k)
\]

Stability score:

\[
A_k = \exp\left(-\frac{G_k}{\tau_A}\right)
\]

If \(G_k\) is high, the candidate state is moving.

That may indicate real drift, a bad lens, nonstationarity, state-boundary failure, or domain change.

---

## 15. Transfer across datasets

Let there be multiple datasets or sources:

\[
X^{a}, X^{b}, X^{c}, ...
\]

Each produces evidence:

\[
Z^a, Z^b, Z^c, ...
\]

### 15.1 Frozen transfer

Transfer validation requires a frozen lens and membership function.

Fit the lens parameters and state membership on reference source \(a\):

\[
L^a = (\phi^a, d_E, \Theta^a, \mathcal{N}^a)
\]

\[
\mu_k^a(z)
\]

Then apply the same frozen lens and membership function to source \(b\):

\[
z_i^b = \phi(W_i^b; \Theta^a)
\]

\[
\mu_k^a(z_i^b)
\]

The transferred evidence distribution is:

\[
P_k^{b|a} = \{z_i^b : \mu_k^a(z_i^b) > \eta\}
\]

The reference evidence distribution is:

\[
P_k^a = \{z_i^a : \mu_k^a(z_i^a) > \eta\}
\]

Transfer distance:

\[
\mathcal{D}_{a \rightarrow b}^{(k)} = D(P_k^a, P_k^{b|a})
\]

Where \(D\) may be:

\[
W_1, W_2, \text{MMD}, \text{JSD}, \text{energy distance}
\]

Directed transfer score:

\[
R_{a \rightarrow b}^{(k)} = \exp\left(-\frac{\mathcal{D}_{a \rightarrow b}^{(k)}}{\tau_R}\right)
\]

Independent refit comparisons are useful rediscovery diagnostics, but they are not transfer validation.

### 15.2 Directed transfer

Frozen transfer is directional.

A state fitted on source \(a\) and applied to source \(b\) is written:

\[
R_{a \rightarrow b}^{(k)}
\]

This is not assumed to equal:

\[
R_{b \rightarrow a}^{(k)}
\]

because the reference source determines the fitted lens parameters, evidence region, prototype, and membership function.

For multiple sources, ShiftLens may report directed all-pairs transfer:

\[
R_k^{directed} = \operatorname{median}_{a \neq b} R_{a \rightarrow b}^{(k)}
\]

and transfer asymmetry:

\[
A_k^{transfer} = \operatorname{median}_{a \neq b}\left|R_{a \rightarrow b}^{(k)} - R_{b \rightarrow a}^{(k)}\right|
\]

High transfer asymmetry indicates reference sensitivity and should weaken any general transfer claim unless explained.

### 15.3 Transfer asymmetry policy

Transfer asymmetry is diagnostic by default. It does not hard-reject a local or temporal state object.

However, transfer asymmetry becomes a gating condition when the state claim is explicitly transferable or state-family level.

For a general all-pairs transferable state claim:

\[
R_k^{directed} \geq R_{min}
\]

and:

\[
A_k^{transfer} \leq A_{max}
\]

must both hold.

If transfer strength is high but asymmetry is also high, the state should be reported as reference-sensitive rather than generally transferable.

### 15.4 Transfer cost policy

Canonical-reference transfer is the default practical transfer protocol:

\[
R_{ref \rightarrow b}^{(k)}
\]

It fits the lens and membership function once on a designated reference source, then applies the frozen state definition to other sources.

Canonical-reference transfer is the default protocol for exploratory work, everyday reporting, and Level 0-2 state claims.

However, canonical-reference transfer is not sufficient for Level 3+ transferable-state or state-family claims, because transfer asymmetry requires directed evidence in both directions.

A Level 3+ claim requires directed all-pairs transfer or an explicitly justified equivalent bidirectional audit protocol:

\[
R_{a \rightarrow b}^{(k)} \quad \text{and} \quad R_{b \rightarrow a}^{(k)}
\]

for source pairs used in the transfer claim.

Therefore, Level 3+ transfer claims must pay the higher validation cost:

\[
O(S^2)
\]

in the number of sources, unless the claim is explicitly limited to a canonical-reference result.

Independent refit comparison remains a rediscovery diagnostic, not transfer validation.

---

## 16. Source fingerprint penalty

A dangerous failure mode is a candidate state that detects source identity rather than a process condition.

Let a classifier try to predict source \(a\) from evidence vectors \(z_i\) inside state \(k\):

\[
\hat{a} = f(z_i)
\]

Source fingerprint score:

\[
\text{fp}_k = \text{BalancedAccuracy}_{CV}(f | S_k) - \text{chance}
\]

where \(\text{BalancedAccuracy}_{CV}\) is cross-validated balanced accuracy over held-out source labels.

Penalty:

\[
\Pi_k^{source} = \max(0, \text{fp}_k)
\]

If this penalty is high, the candidate may be detecting the dataset, generator, instrument, environment, or source rather than a reusable state.

---

## 17. Null model and rejection model

A candidate state must beat a null.

Define a null generator:

\[
\mathcal{N}
\]

It creates negative-control datasets:

\[
X^{null,1}, X^{null,2}, ..., X^{null,M}
\]

Examples include:

- time shuffle;
- block shuffle;
- phase randomization;
- label permutation;
- surrogate noise with the same marginal distribution;
- synthetic negative-control generation.

For any evidence score \(E_k\), compute the null distribution:

\[
E_k^{null} = \{E_k^{null,1}, ..., E_k^{null,M}\}
\]

Raw state significance:

\[
p_k = P(E_k^{null} \geq E_k)
\]

A serious state claim should survive a vector of tests, not one score alone.

### 17.1 Multiple-testing correction

When multiple candidate states are tested, raw p-values are diagnostic only.

Let the candidate set be:

\[
\mathcal{C} = \{S_1, S_2, ..., S_K\}
\]

with raw p-values:

\[
p_1, p_2, ..., p_K
\]

Define corrected values:

\[
q_k = \text{Adjust}(p_k, K)
\]

For exploratory discovery, Benjamini-Hochberg false discovery rate correction is preferred unless a stricter family-wise error control is required.

State validation uses corrected q-values:

\[
q_k < \alpha
\]

not raw p-values alone.

---

## 18. Evidence vector

For each candidate state:

\[
\mathbf{e}_k = [s_k, C_k, B_k, Q_k, P_k, A_k, R_k, 1-\Pi_k^{source}]
\]

Where:

| Term | Meaning |
|---|---|
| \(s_k\) | support |
| \(C_k\) | internal coherence |
| \(B_k\) | external separation |
| \(Q_k\) | boundary confidence |
| \(P_k\) | temporal persistence |
| \(A_k\) | stability over time |
| \(R_k\) | transfer/reproducibility |
| \(1-\Pi_k^{source}\) | resistance to source fingerprinting |

A state has an evidence profile, not just a grade.

---

## 19. Visibility score

A scalar summary can be useful, but it must not replace the evidence profile.

Define clipped evidence terms:

\[
\tilde{e}_{kl} = \min(1-\epsilon, \max(\epsilon, e_{kl}))
\]

where:

\[
0 < \epsilon \ll 1
\]

Then define visibility:

\[
V_k = \prod_l \tilde{e}_{kl}^{w_l}
\]

where all weights are non-negative:

\[
w_l \geq 0
\]

For numerical stability, use log form:

\[
\log V_k = \sum_l w_l \log \tilde{e}_{kl}
\]

The clipped scalar visibility score is for ranking and reporting. Hard gates remain separate.

A state should not be validated merely because its scalar visibility score is high, and a state should not be silently destroyed by one near-zero numerical term unless that term also fails an explicit hard gate.

Plain interpretation:

```text
A state is more visible when it is supported, coherent, separated,
persistent, stable, transferable, and resistant to trivial source explanations.
```

---

## 20. Statehood test

A candidate becomes a validated state object only if:

\[
s_k \geq s_{min}
\]

\[
C_k \geq C_{min}
\]

\[
B_k \geq B_{min}
\]

\[
P_k \geq P_{min}
\]

\[
q_k < \alpha
\]

and no hard rejection applies.

Define:

\[
\mathcal{T}(S_k) = \mathbf{1}[s_k \geq s_{min} \land C_k \geq C_{min} \land B_k \geq B_{min} \land P_k \geq P_{min} \land q_k < \alpha \land \neg \text{HardReject}(S_k)]
\]

Then:

\[
S_k \in \text{ValidatedStates}
\]

if and only if:

\[
\mathcal{T}(S_k)=1
\]

Transfer gates apply according to the level of claim being made. A local or temporal state claim does not require the same transfer evidence as a Level 3+ transferable-state claim.

---

## 21. Rejection function

Define rejection as:

\[
\mathcal{J}(S_k) \rightarrow \{\text{reasons}\}
\]

More precisely:

\[
\mathcal{J}(S_k) \subseteq \mathcal{R}
\]

where \(\mathcal{R}\) is the set of rejection reasons.

Examples:

\[
\mathcal{J}(S_k) =
\begin{cases}
\text{insufficient\_support} & s_k < s_{min} \\
\text{poor\_coherence} & C_k < C_{min} \\
\text{poor\_separation} & B_k < B_{min} \\
\text{temporal\_flicker} & P_k < P_{min} \\
\text{source\_fingerprint} & \Pi_k^{source} > \Pi_{max} \\
\text{non\_reproducible} & R_k < R_{min} \\
\text{unstable\_region} & A_k < A_{min}
\end{cases}
\]

A candidate can have multiple rejection reasons.

Rejection is not just failure. Rejection is evidence.

---

## 22. Dirty state detection

A dirty state is not necessarily fake.

A dirty state is repair-worthy but incoherent. It has enough support to be worth investigating, fails internal structure, and still has separation or persistence evidence strong enough to suggest real structure may be recoverable.

Define dirty state condition:

\[
\text{Dirty}(S_k) =
\left[
s_k \geq s_{min}
\land
C_k < C_{min}
\land
(B_k \geq B_{dirty} \lor P_k \geq P_{dirty})
\right]
\]

Where:

- \(B_{dirty}\) is the minimum separation evidence for dirty-state suspicion.
- \(P_{dirty}\) is the minimum persistence evidence for dirty-state suspicion.
- \(B_{dirty}\) and \(P_{dirty}\) are weaker repair-diagnostic thresholds, not full validation thresholds.

Threshold constraints:

\[
0 \leq B_{dirty} < B_{min}
\]

\[
0 \leq P_{dirty} < P_{min}
\]

A simple default rule is:

\[
B_{dirty} = \alpha_B B_{min}, \quad 0 < \alpha_B < 1
\]

\[
P_{dirty} = \alpha_P P_{min}, \quad 0 < \alpha_P < 1
\]

where \(\alpha_B\) and \(\alpha_P\) are lens-level repair sensitivity parameters. Lower values make dirty-state suspicion more permissive; higher values make it closer to validation strictness.

A dirty state is not validated statehood. It is a repair candidate: enough structure exists to justify repair, but the candidate fails coherence.

An overloaded state can be defined as:

\[
\text{Overloaded}(S_k) =
\left[
|\mathcal{D}_{over}| \geq n_{over}^{min}
\land
\sigma_k^2 \geq \sigma^2_{over}
\land
\exists (S_{k1}, S_{k2}) :
s_{k1} \geq s_{min}
\land
s_{k2} \geq s_{min}
\land
\Delta V_{split} \geq \delta_{split}
\right]
\]

Where:

- \(\mathcal{D}_{over}\) is the supported-candidate dispersion cohort used to set the overloaded-state threshold.
- \(n_{over}^{min}\) is the minimum cohort size required before evaluating a cohort-relative overloaded-state threshold.
- \(\sigma^2_{over}\) is the dispersion threshold for overloaded-state suspicion.
- \(\delta_{split}\) is the minimum required mass-weighted improvement from a split after the complexity penalty.
- \(S_{k1}\) and \(S_{k2}\) are proposed child candidates of \(S_k\).

\[
n_{over}^{min} \geq 2
\]

\[
\mathcal{D}_{over} = \{\sigma_j^2 : s_j \geq s_{min}\}
\]

\[
\sigma^2_{over} =
q_{over}(\mathcal{D}_{over})
\quad
\text{only if}
\quad
|\mathcal{D}_{over}| \geq n_{over}^{min}
\]

where \(q_{over}\) is a high quantile selected by the lens, such as the 0.75 or 0.90 quantile. This makes overloaded-state suspicion relative to the dispersion profile of supported candidates under the same lens.

If \(|\mathcal{D}_{over}| < n_{over}^{min}\), the cohort-relative overloaded-state gate is not evaluated. In that sparse-cohort case, \(\text{Overloaded}(S_k)\) defaults to false under the cohort-relative rule. The candidate may still be reported as dirty, unstable, unknown, or requiring more evidence, but it is not labelled overloaded from an undefined cohort quantile.

A configured absolute \(\sigma^2_{over}\) threshold may be used instead only if it is explicitly declared by the lens or report policy.

\[
\delta_{split} > 0
\]

A practical default is:

\[
\delta_{split} = \max(\epsilon_V, \eta_{split} n_k V_k)
\]

where \(\epsilon_V > 0\) is the smallest meaningful evidence-improvement margin and \(\eta_{split} > 0\) is the minimum proportional gain required before accepting a split proposal.

Valid split proposals must satisfy child support requirements and the mass-weighted improvement requirement. A split that improves only one local score but fails \(\Delta V_{split} \geq \delta_{split}\) is not enough to mark a candidate overloaded.

An overloaded state has thresholded evidence that the candidate contains multiple supported sub-states. It is not automatically validated statehood; it is a split-repair candidate.

\(\Delta V_{split}\) is the mass-weighted split improvement defined in §22.1.

### 22.1 Mass-weighted split improvement

Split improvement should be mass-weighted and should pay a subtractive complexity penalty:

\[
\Delta V_{split} = (n_{k1}V_{k1} + n_{k2}V_{k2}) - n_kV_k - \lambda_{split}\operatorname{Complexity}(k \rightarrow k1,k2)
\]

A split is favoured only if mass-weighted evidence improves after paying the complexity penalty, and each child candidate satisfies minimum support requirements:

\[
s_{k1} \geq s_{min}
\]

\[
s_{k2} \geq s_{min}
\]

This prevents unsupported over-splitting.

---

## 23. Merge test

Two states should be considered for merging if separation is too low and the merged candidate improves evidence.

Merge candidate:

\[
S_{ij} = S_i \cup S_j
\]

Mass-aware merge improvement:

\[
\Delta V_{merge} = n_{ij}V_{ij} - (n_iV_i+n_jV_j) - \lambda_{merge}\operatorname{Complexity}(i,j \rightarrow ij)
\]

Merge if:

\[
\Delta V_{merge} > 0
\]

and:

\[
\Delta_{ij} < \Delta_{min}
\]

Plain interpretation:

```text
These candidates are not meaningfully separate states.
```

Split and merge tests both use mass-weighted evidence and subtractive complexity penalties.

---

## 24. Unknown-real candidate

A fake state and an unknown real state can both look wrong.

ShiftLens must preserve the distinction.

Define unknown-real candidate:

\[
\text{UnknownCandidate}(S_k)
\]

if local evidence is strong:

\[
s_k \geq s_{min}
\]

\[
C_k \geq C_{min}
\]

\[
P_k \geq P_{min}
\]

but transfer fails:

\[
R_k < R_{min}
\]

or transfer fails in a structured way.

Structured failure means the failure pattern is not random under null:

\[
p(\text{transfer failure pattern}) < \alpha
\]

So:

\[
\text{UnknownCandidate}(S_k) = [\text{local evidence strong} \land \text{transfer failure significant} \land \text{source fingerprint not sufficient explanation}]
\]

Plain interpretation:

```text
This might not be fake.
It may be a real condition the current model does not understand yet.
```

---

## 25. Repair operator

Define a repair operator:

\[
\rho \in \mathcal{P}
\]

where \(\mathcal{P}\) is the repair action set:

\[
\mathcal{P} = \{\text{split}, \text{merge}, \text{rebound}, \text{change lens}, \text{change window}, \text{isolate transition}, \text{mark unknown}, \text{reject}\}
\]

Repair is selected by expected evidence improvement:

\[
\rho^* = \arg\max_{\rho \in \mathcal{P}} \Delta V(\rho(S_k))
\]

where:

\[
\Delta V(\rho(S_k)) = V(\rho(S_k)) - V(S_k)
\]

To avoid overfitting, add a subtractive complexity penalty:

\[
\rho^* = \arg\max_{\rho} [\Delta V(\rho(S_k)) - \lambda \cdot \text{Complexity}(\rho)]
\]

This prevents the system from endlessly splitting states until every point becomes its own state.

---

## 26. State lifecycle

The full mathematical lifecycle is:

\[
X \rightarrow W \rightarrow Z \rightarrow \{S_k^{candidate}\} \rightarrow \mathbf{e}_k \rightarrow \mathcal{J}(S_k) \rightarrow \rho(S_k) \rightarrow S_k^{validated} \text{ or } S_k^{rejected}
\]

Plain version:

```text
raw series
→ windows
→ evidence space
→ candidate regions
→ evidence vector
→ rejection test
→ repair test
→ validated / rejected / unknown
```

Extractor and critic must remain separate:

\[
\text{Extractor} \neq \text{Critic}
\]

\[
\text{Candidate generation} \neq \text{State validation}
\]

The extractor produces candidates. The critic determines how much statehood the candidate has earned.

---

## 27. Hierarchy of state claims

### Level 0 — Candidate evidence-region

\[
S_k^{0}
\]

Exists when:

\[
R_k \subseteq \mathcal{E}
\]

Meaning:

```text
A region was found.
No strong claim yet.
```

### Level 1 — Supported state candidate

\[
S_k^{1}
\]

Exists when support, coherence, and separation clear minimum thresholds.

Meaning:

```text
The region has evidence.
```

### Level 2 — Temporal state object

\[
S_k^{2}
\]

Exists when persistence and transition tests show temporal structure.

Meaning:

```text
The region behaves like a process condition over time.
```

Canonical-reference transfer may be reported at this level as exploratory transfer evidence, but it does not establish a general transferable-state claim.

### Level 3 — Transferable state object

\[
S_k^{3}
\]

Exists when directed all-pairs transfer or an explicitly justified equivalent bidirectional audit passes the transfer-strength and transfer-asymmetry gates.

Meaning:

```text
The state appears beyond one dataset or source under bidirectional transfer audit.
```

### Level 4 — State family

\[
F_k
\]

Exists when multiple validated transferable states share a structural signature:

\[
F_k = \{S_k^a,S_k^b,S_k^c,...\}
\]

with:

\[
d_F(S_k^a,S_k^b) < \epsilon_F
\]

Meaning:

```text
Reusable state family across datasets, sources, or domains.
```

---

## 28. Compact mathematical definition

\[
X \in \mathbb{R}^{T \times d}
\]

\[
W_i = X_{i:i+m-1}
\]

\[
z_i = \phi(W_i; \Theta)
\]

\[
R_k \subseteq \mathcal{E}
\]

\[
\mu_k(z_i) \in [0,1]
\]

\[
S_k = \{(W_i,z_i,\mu_k(z_i))\}_{i=1}^{N}
\]

\[
\mathbf{e}_k = [s_k, C_k, B_k, Q_k, P_k, A_k, R_k, 1-\Pi_k^{source}]
\]

\[
\tilde{e}_{kl} = \min(1-\epsilon, \max(\epsilon, e_{kl}))
\]

\[
V_k = \prod_l \tilde{e}_{kl}^{w_l}
\]

\[
\mathcal{J}(S_k) \subseteq \mathcal{R}
\]

\[
S_k \text{ is validated iff } \mathcal{T}(S_k)=1
\]

Validation requires claim-appropriate evidence, including:

- support;
- coherence;
- separation;
- boundary confidence;
- temporal persistence;
- stability;
- corrected q-values;
- low source fingerprint;
- null-model survival;
- explicit rejection record;
- transfer evidence when the claim requires transfer.

---

## 29. Core law

```text
No state without evidence.
No evidence without reproducibility.
No reproducibility without rejection.
No rejection without repair path.
No repair path without source trace.
```

Sharper:

```text
A hidden state is not found until it can survive being attacked.
```

---

## 30. One-sentence mathematical summary

\[
\boxed{\text{A ShiftLens state is a fuzzy evidence-region over time-indexed windows whose claim strength is determined by support, coherence, separation, persistence, transfer, stability, and rejection survival.}}
\]

Even shorter:

\[
\boxed{S_k \neq R_k;\quad S_k = R_k + \mathbf{e}_k + \mathcal{J}(S_k)}
\]

Meaning:

```text
A state is not just a region.
A state is a region plus evidence plus its own failure conditions.
```

---

## 31. First implementation implication

The first implementation layer should define the state-evidence objects before adding advanced extractors.

Suggested core objects:

```text
Lens
EvidenceRegion
StateCandidate
StateEvidence
StateCritic
RejectionReason
RepairAction
StateReport
```

The baseline extractor should be treated as one simple candidate generator, not the identity of the project.

```text
BaselineExtractor -> StateCandidate[]
StateCritic -> StateEvidence[]
ReportWriter -> reproducible report
```

The long-term architecture is:

```text
extractor produces candidates
critic produces trust
report preserves evidence
```

---

## 32. Use of standard methods

This framework uses standard statistical and time-series concepts, including windowing, feature maps, metric spaces, fuzzy membership, null testing, multiple-testing correction, transfer validation, and source-fingerprint diagnostics.

The contribution of this document is the ShiftLens statehood contract: a candidate state is not accepted merely because an extractor labels it. A candidate earns statehood only by surviving evidence, rejection, repair, and transfer tests appropriate to the claim being made.

---

## 33. Final working definition

ShiftLens is a state-evidence framework for time-series systems.

It treats hidden states as candidate structural conditions, not labels.

A candidate state becomes useful only when ShiftLens can attach evidence: support, coherence, separation, persistence, transition behaviour, transfer behaviour, rejection reasons, repair paths, and reproducible source traces.

The purpose of ShiftLens is to make hidden states visible enough that they can be tested, rejected, repaired, compared, and eventually reused as scientific or engineering objects.
