# Part C — Multilingual Casual-Response Recommendation Memo

## Recommendation

**Choose (b): a local inference-time rewriter ≤1B parameters**, placed after the main model and before the response is shown to the user. Use it to rewrite formal/generated responses into casual conversational Hindi, Kannada, Tamil, Telugu, Bengali, and Marathi while preserving meaning. Keep the main model unchanged so the feature is reversible and can be disabled independently.

## Assumptions

- 6 target languages: Hindi, Kannada, Tamil, Telugu, Bengali, Marathi.
- Synthetic data target: **2,000 response pairs/language = 12,000 pairs**.
- Average pair size: **60 input + 60 target tokens = 120 tokens/pair**.
- Fine-tuning uses LoRA/parameter-efficient tuning on one A100-80GB.
- Effective training throughput is assumed at **150 tokens/s**; this is a planning estimate and must be measured in the day-1 experiment.
- Native-speaker review capacity is assumed at **30 examples/hour**.

## Back-of-the-envelope cost / effort

**Data:**  
12,000 pairs × 120 tokens = **1.44M training tokens**.  
At 3 epochs: 1.44M × 3 = **4.32M training tokens**.

**Training:**  
4.32M / 150 tokens/s ≈ **8 GPU-hours** for one training run.  
Reserve **48 A100 GPU-hours** for multiple runs, evaluation and checkpointing, which is 48 / (14 × 24) ≈ **14%** of the available two-week GPU window.

**Serving:**  
A 1B-parameter FP16 rewriter requires approximately **2 GB for weights**, before runtime/KV overhead. An A100-80GB can therefore host it alongside the application stack. Assuming a 60-token rewrite and 20 generated tokens/s, rewrite latency is approximately **3 seconds**; this is an assumption that must be measured before launch.

**Human review:**  
10 h/week × 2 weeks = **20 reviewer-hours**.  
20 × 30 examples/hour = **600 reviewed examples**, or about **300 each for Hindi and Kannada**. The reviewer cannot provide equivalent native-speaker validation for Tamil, Telugu, Bengali and Marathi, which is the largest launch risk.

## Why not the other options?

- **(a) SFT the main model:** potentially strongest integration, but it changes the production model, requires more validation and creates a harder rollback path under a three-week launch schedule.
- **(c) Prompt engineering only:** cheapest and fastest baseline, but gives less reliable control over casual style across six languages and should be treated as the day-1 baseline rather than the final solution.

## Success threshold and kill criterion

Launch only if the rewriter achieves **≥85% casual-natural pass rate** on the reviewed Hindi/Kannada holdout, with **<5% critical meaning-changing rewrites**.

**Kill criterion:** by the end of **Day 5**, stop the rewriter approach if casual-natural pass rate is **<70%** or critical meaning changes are **>5%**. Fall back to the best prompt-only baseline while investigating the failure.

## Day-1 experiment

Create a fixed 100-example holdout per language and compare:

1. main model + prompt engineering;
2. main model + local ≤1B rewriter.

Measure casual-style pass rate, meaning preservation, rewrite latency and output-token overhead. Review Hindi and Kannada manually; use automated checks for the other four languages until additional native-speaker validation is available.

## Biggest caveat

The **single reviewer only covers Hindi and Kannada**, so a strong result on those languages cannot establish equivalent quality for Tamil, Telugu, Bengali and Marathi. The launch decision should therefore explicitly treat the four unreviewed languages as residual risk rather than claiming six-language human validation.