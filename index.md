---
title: A Brain-Wide Atlas of Intrinsic Neural Timescales in Mice
authors:
  - name: Süheyl Berat Gülenç
  - name: Kayla Stafford
  - name: Zhiyi Yang
  - name: Vikramaditya Bisani
bibliography:
  - bib.bib
---

## Abstract

Understanding how the brain integrates information requires a shift from localized functional studies to mapping a brain-wide temporal architecture. Intrinsic neural timescales (ITs), defined as the decay time constant of a neuron's spontaneous spiking autocorrelation, provide a quantitative proxy for how long a local circuit retains information about its recent activity. Yet their accurate estimation has historically been limited by computational biases in spike train analysis and the oversimplified assumption that each neuron operates on a single characteristic timescale. In this study, we address these limitations by applying a hybrid framework combining the unbinned intrinsic Spike Time Tiling Coefficient (iSTTC) autocorrelation estimator with Bayesian Information Criterion (BIC)-guided multi-exponential modeling to 89,047 single units across 266 mouse brain regions. We confirm a rostro-caudal timescale gradient, with the median effective timescale approximately 4.5-fold longer in the hindbrain (956 ms) than in the forebrain (213 ms), consistent with recent brain-wide mapping efforts. We further demonstrate that 73.9% of neurons are better described by multi-component models, and find that fast ($\tau_1$) and slow ($\tau_2$) dynamical modes co-vary sublinearly across regions. These findings lay the groundwork for future analyses linking single-neuron dynamics to the emergence of stable, population-level representations required for decision making and adaptive behavior.

**Keywords:** Intrinsic Timescales, Brain-Wide Mapping, Multi-Exponential Modeling, Neural Dynamics

## Introduction

Intrinsic neural timescales ($\tau$) describe how long neuronal activity remains correlated with its own past. Fast (short-$\tau$) regions respond rapidly to sensory inputs, while slow (long-$\tau$) regions sustain activity across delays, supporting evidence accumulation and memory {cite}`murray2014,wasmuht2018`. Quantified as the decay time constant of spontaneous spiking autocorrelation, intrinsic neural timescales have emerged as a fundamental metric of this process {cite}`murray2014`. Longer timescales are thought to underlie cognitive computations that require information to be maintained over time, including working memory, evidence accumulation, and decision making.

However, constructing a brain-wide map of timescales presents significant methodological challenges. Classical binned autocorrelation functions (ACFs) systematically underestimate timescales for neurons with low firing rates or bursty dynamics, conditions common across subcortical and hindbrain regions. Furthermore, fitting a single exponential decay assumes each neuron operates on only one characteristic timescale, obscuring the multi-component temporal architecture present in the majority of neurons. To address both limitations, we apply iSTTC, an unbinned estimator that computes autocorrelations directly from exact spike times, alongside BIC-guided multi-exponential modeling. This combination extends anatomical coverage to regions that classical methods would exclude, and resolves the coupled fast-slow dynamical architecture that single-exponential methods obscure entirely.

The IBL dataset is uniquely suited for this analysis: its brain-wide Neuropixels coverage, 5–10 minute spontaneous activity recordings, and standardized decision-making task allow timescale estimates to be paired with neural dynamics during the decision epoch across nearly all major brain structures. The multi-component modeling framework reveals that 73.9% of neurons carry both fast and slow dynamical modes simultaneously, providing the mechanistic resolution needed to ask not just where timescales are long, but how the interplay between fast and slow modes relates to the stability of neural activity and behavioral decisions across the whole brain.

## Results

We analyzed spontaneous spiking activity from 580,598 units across 266 brain regions drawn from the IBL 2025 Brainwide Map Release (see [Supplementary Methods](#supplementary-methods) for full quality criteria, iSTTC derivation, and model selection procedure).

Despite this within-region heterogeneity, a clear anatomical gradient emerged when neurons were grouped by major division. The forebrain exhibited the shortest timescales (median $\tau_\text{eff}$ = 213 ms, IQR = 120–304 ms), while the midbrain and hindbrain showed markedly longer temporal persistence (765 ms, IQR = 482–968 ms and 956 ms, IQR = 723–1183 ms, respectively) ([Figure 1A](#figure-main)). This rostro-caudal hierarchy is consistent with independent estimates reported by {cite}`shi2025`, providing cross-study validation of this gradient. This forebrain-to-hindbrain organisation was further reflected at the level of individual Beryl subdivisions, with hippocampal and cortical subplate regions anchoring the fast end and hindbrain nuclei clustering at the slow extreme ([Figure 1B](#figure-main)) {cite}`ibl_atlas`.

```{figure} figure.png
:name: figure-main
:align: center
:alt: Brain-wide map of intrinsic neural timescales across brain regions

**Brain-wide map of intrinsic neural timescales across brain regions.** All panels except C exclude regions with fewer than 15 neurons (220 regions retained); C excludes regions with fewer than 5 neurons (244 regions retained). **(A)** Effective timescale distributions by major brain division (forebrain, midbrain, hindbrain); boxes show the interquartile range of region-level $\tau_\text{eff}$ medians, with whiskers extending to the 10th and 90th percentiles. **(B)** Timescale distributions across the 12 Beryl parcellation subdivisions, ordered from fastest to slowest median $\tau_\text{eff}$. Boxes show the interquartile range and whiskers indicate the 10th and 90th percentiles. **(C)** Brain-wide bar chart of median $\tau_\text{eff}$ per region; bars show median $\tau_\text{eff}$ and error bars indicate the interquartile range (Q1–Q3). Regions are grouped by major anatomical division — forebrain (top), midbrain (middle), and hindbrain (bottom) — and ordered alphabetically within each subdivision. Colour denotes Allen Mouse Brain Atlas Beryl parcellation subdivision (CTX, isocortex; OLF, olfactory areas; HPF, hippocampal formation; CTXsp, cortical subplate; STR, striatum; PAL, pallidum; TH, thalamus; HY, hypothalamus; P, pons; MY, medulla; MB, midbrain; CB, cerebellum). **(D)** Coupled multiscale architecture of fast and slow timescale components. Each point represents one brain region ($n$ = 220 regions with reliable two-component fits), plotted by its median fast timescale ($\tau_1$) against its median slow timescale ($\tau_2$) on log-log axes. Colors denote major division: forebrain, midbrain, and hindbrain. The dashed line shows the log-log regression fit (slope = 0.545, $r$ = 0.766, $p$ = 9.68 × 10⁻⁴⁴), indicating that regions with longer fast timescales also tend to have proportionally longer slow timescales.
```

To confirm that the anatomical hierarchy is observable within individual mice, we fitted a linear mixed-effects model with Beryl region as a fixed effect and mouse identity as a random intercept ($n = 77{,}328$ neurons, 131 mice; [Supplementary Methods](#supplementary-methods)). Brain region explained 31.4% of variance in $\log_{10}(\tau_\text{eff})$ (cross-validated $R^2 = 0.309$; LRT $\chi^2(265) = 22{,}698$, $p < 0.001$).

Mouse identity accounted for 13.8% of total variance before accounting for region but only 5.9% after, indicating that apparent inter-mouse variability largely reflects differences in anatomical sampling ([Supplementary Table 1a](#supp-table-1a)). Among 56 mice contributing neurons to at least four Beryl subdivisions, 100% showed shorter forebrain than hindbrain timescales, with within-mouse rank orderings correlating strongly with the population-level hierarchy (median Spearman $\rho = 0.76$, $p < 10^{-30}$).

A Bayesian hierarchical model with region, mouse, session, and probe as random intercepts yielded consistent results, with posterior estimates strongly supporting longer intrinsic timescales in midbrain and hindbrain relative to forebrain (forebrain < midbrain, $p = 1.0 \times 10^{-4}$; forebrain < hindbrain, $p = 1.6 \times 10^{-7}$), while largely preserving the subdivision-level ordering observed in the main population-level analysis (Spearman $\rho = 0.895$, $p < 0.001$; [Supplementary Methods](#supplementary-methods)).

Many neurons were best described by multi-timescale models, raising the question of whether fast and slow components are independently organized or jointly constrained. We therefore examined how $\tau_2$ co-varies with $\tau_1$ across regions, restricting the analysis to neurons best described by exactly two components (60.4%). $\tau_2$ co-varied strongly with $\tau_1$ ($r = 0.78$, $p < 10^{-26}$; [Figure 1D](#figure-main)), following a sublinear relationship (slope = 0.69), consistent with coordinated scaling of fast and slow dynamics across brain regions.

## Discussion

Our findings extend prior brain-wide timescale mapping by demonstrating that the rostro-caudal gradient holds in a substantially larger and more recent IBL dataset, and by resolving the multi-component temporal structure that single-exponential methods obscure. The longer timescales of midbrain and hindbrain structures may reflect their roles in integrating homeostatic, motor, and state-related signals over extended periods {cite}`grill2012,caggiano2018`.

The sublinear co-variation between $\tau_1$ and $\tau_2$ across all major divisions suggests that fast and slow integration windows are co-regulated rather than independent, consistent with the view that synaptic time constants jointly constrain multiple dynamical modes within a region {cite}`beiran2019,fontanier2022`. This coupling implies a shared biophysical substrate simultaneously shaping the speed and depth of temporal integration, a constraint that single-exponential summaries cannot detect.

The substantial within-region variance in $\tau_\text{eff}$ (median IQR = 588 ms per area) warrants attention in future work. Regional medians may obscure meaningful neuron-to-neuron heterogeneity that is functionally relevant, motivating analyses of full timescale distributions within regions rather than summary statistics alone.

## Limitations

While our hybrid approach resolves key biases, some limitations remain. Estimating ultra-slow timescales ($\tau$ > 2,000 ms) yields wide confidence intervals due to the inherent limit of the ~10-minute recording epoch. Additionally, regions dominated by highly regular oscillatory dynamics (such as theta rhythms in the hippocampus) exhibited lower fit qualities ($R^2$), as sum-of-exponentials models cannot fully capture non-monotonic ACF structures.

Because intrinsic timescales were estimated from the full spontaneous epoch, early passive-state transients may contribute to the estimates. When the passive period begins, the mouse has just finished performing the decision-making task, and residual task-related signals may persist for tens of seconds into the passive epoch, potentially biasing $\tau_\text{eff}$ upward in regions strongly recruited by the task. Future robustness analyses should test whether excluding the first 60–120 s of spontaneous activity changes the observed anatomical hierarchy.

## Acknowledgments

This research was conducted as part of Neuromatch's Impact Scholars Program. We thank the International Brain Laboratory for the publicly available Neuropixels dataset, and acknowledge the methodological frameworks developed by {cite}`pochinok2026` and {cite}`shi2025`.

## References

```{bibliography}
```

---

(supplementary-methods)=
## Supplementary Methods

**Dataset and unit selection.** We analyzed spontaneous spiking activity from 580,598 recorded units across 427 sessions, 651 probes, 131 mice, and 266 brain regions using the open-access IBL 2025 Brainwide Map Release {cite}`ibl2025` Neuropixels dataset, focusing on the 5–10 minute passive resting state epochs for computing intrinsic timescales.

Units were retained for analysis if they met all of the following quality criteria: ≥100 spontaneous spikes, a declining iSTTC autocorrelation in the 50–200 ms window, multi-exponential fit $R^2$ ≥ 0.5, 95% confidence interval of $\tau_\text{eff}$ excluding zero, and $\tau_\text{eff}$ below the upper bound of the exponential fitting range (30,000 ms). Following these criteria, 89,047 viable units (representing 15.34% of the initial population) were retained for downstream analysis.

**iSTTC estimator.** iSTTC estimates the autocorrelation-like function by generating temporally shifted copies of each spike train and computing the Spike Time Tiling Coefficient (STTC) between the original and shifted versions at successive lags ($\Delta t$ = 5 ms, 600–1200 lags). Because STTC operates directly on exact spike times rather than binned counts, it is insensitive to zero-padding artifacts and does not require a minimum firing rate threshold. We confirmed that iSTTC-derived $\tau_\text{eff}$ estimates showed no systematic dependence on firing rate across the analyzed population ([Supplementary Figure 2](#supp-fig-2)).

**Multi-exponential model fitting and component selection.** To address the limitations of single-exponential assumptions, we fitted each neuron's iSTTC autocorrelation curve with a sum of $M$ exponential decay components ($M$ = 1–4):

$$f(t) = \sum_i c_i \cdot \exp(-t/\tau_i)$$

The optimal $M$ was selected via the Bayesian Information Criterion (BIC), with the constraint that each component contributed at least 1% to the overall autocorrelation shape. The amplitude-weighted average of the fitted components yielded $\tau_\text{eff} = \sum_i c_i \tau_i / \sum_i c_i$, enabling direct comparison across neurons regardless of dynamical complexity. For the $\tau_1$–$\tau_2$ coupling analysis, neurons fitted by three or more components (13.8%) were excluded.

## Supplementary Figures

```{figure} figures/figure_s1.png
:name: supp-fig-1
:align: center
:alt: Distribution of the number of timescale components per neuron

**Distribution of the number of timescale components per neuron.**
The majority of well-fitted neurons were best described by two-timescale models (60.4%), followed by one-timescale (25.7%) and three-timescale (13.8%) models, with only 0.1% requiring four timescales. The optimal number of components was selected using the Bayesian information criterion (BIC), with the constraint that each component contributed at least 1% to the overall autocorrelation shape.
```

```{figure} figures/figure_s2.png
:name: supp-fig-2
:align: center
:alt: Effective intrinsic timescale as a function of firing rate

**Effective intrinsic timescale as a function of firing rate.**
Distribution of $\tau_\text{eff}$ across neurons grouped into firing rate bins (IQR shown as box height, median as horizontal line, log scale on both axes). Contrary to the expectation that high firing rates would trivially produce short timescales, no simple inverse relationship is observed: median $\tau_\text{eff}$ is lowest in the <1 Hz bin and rises across intermediate firing rates, with the highest median values in the 20–50 and >50 Hz bins. The broad IQR within each bin further indicates that firing rate is a poor predictor of $\tau_\text{eff}$ at the single-neuron level.
```

```{figure} figures/figure_s3.png
:name: supp-fig-3
:align: center
:alt: Population distribution of effective intrinsic timescales

**Population distribution of effective intrinsic timescales.**
Histogram of $\tau_\text{eff}$ across all well-fitted neurons (log-scaled x-axis), revealing a broad, right-skewed distribution with a mode near 800 ms and a heavy tail extending beyond 1,000 ms.
```

(supp-table-1a)=
## Supplementary Tables

**Supplementary Table 1a: Nested variance decomposition.** Proportion of variance in $\log_{10}(\tau_\text{eff})$ attributable to each level of the data hierarchy, estimated before and after including Beryl region (266 levels) as a fixed effect. The reduction in mouse and session variance after adding region indicates that apparent inter-individual variability largely reflects differences in anatomical sampling across recordings.

| Source | Within region | With region fixed effect |
|--------|:-------------:|:------------------------:|
| Mouse | 13.8% | 5.9% |
| Session (within mouse) | 13.6% | 6.6% |
| Probe (within session) | 6.2% | 2.4% |
| Neuron residual | 66.5% | 85.1% |

**Supplementary Table 1b: Mixed-effects model results across parcellation levels.** Variance explained ($R^2$) and significance of the anatomical gradient at three levels of granularity, with mouse identity as a random intercept. CV $R^2$ denotes 5-fold cross-validated $R^2$ (mean ± s.d.). Mouse var (%) is the proportion of total variance captured by the mouse random intercept in each model. LRT: likelihood ratio test of the anatomical fixed effect against a null model with random intercept only.

| Parcellation level | Number of divisions | $R^2$ | CV $R^2$ | Mouse var (%) | LRT $\chi^2$ (df) | $p$ |
|--------------------|:-------------------:|:-----:|:---------:|:-------------:|:-----------------:|:---:|
| Major division (forebrain/midbrain/hindbrain) | 3 | 0.189 | 0.189 ± 0.007 | 10.2 | 11,072 (2) | < 0.001 |
| Beryl subdivision (e.g., isocortex, hippocampal formation) | 12 | 0.254 | 0.254 ± 0.005 | 9.5 | 16,996 (11) | < 0.001 |
| Beryl region (e.g., CA1, VISp, MRN) | 266 | 0.314 | 0.309 ± 0.004 | 8.0 | 22,698 (265) | < 0.001 |