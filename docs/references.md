# References

## Foundational papers

### Prompt injection attacks & defenses

- **Liu et al.**, "Formalizing and Benchmarking Prompt Injection Attacks and
  Defenses" (USENIX Security 2024).
  *a.k.a. Open Prompt Injection.* — The formalization most of pikit's attacks
  and defenses follow.

- **Greshake et al.**, "Not what you've signed up for: Compromising Real-World
  LLM-Integrated Applications with Indirect Prompt Injection" (AISec 2023).
  — Introduced indirect prompt injection, the core threat model for pikit's
  channels and agent testbed.

- **Hines et al.**, "Defending Against Indirect Prompt Injection Attacks With
  Spotlighting" (Microsoft, 2024).
  — Source of pikit's `spotlighting` defense (datamarking / encoding / marking
  modes).

### Related frameworks

- **foolbox** — A Python toolbox for adversarial attacks on machine learning
  models. [github.com/bethgelab/foolbox](https://github.com/bethgelab/foolbox)
- **cleverhans** — An adversarial examples library for ML.
  [github.com/cleverhans-lab/cleverhans](https://github.com/cleverhans-lab/cleverhans)
- **TextAttack** — A framework for adversarial attacks in NLP.
  [github.com/QData/TextAttack](https://github.com/QData/TextAttack)
- **EasyJailbreak** — A unified framework for jailbreaking LLMs.
  [github.com/EasyJailbreak/EasyJailbreak](https://github.com/EasyJailbreak/EasyJailbreak)

## Attack method mapping

| pikit key | Technique | Source |
|---|---|---|
| `naive` | Direct concatenation | Baseline |
| `escape` | Escape characters to break context | Open Prompt Injection |
| `context_ignoring` | "Ignore previous instructions" | Open Prompt Injection |
| `fake_completion` | Forge a completion + new instruction | Open Prompt Injection |
| `combined` | fake-completion + escape + context-ignoring | Open Prompt Injection (strongest baseline) |
| `payload_splitting` | Split payload into fragments | Open Prompt Injection |
| `obfuscation` | base64 / leetspeak encoding | Open Prompt Injection |
| `prompt_leaking` | System prompt extraction | Open Prompt Injection |
| `prefix_injection` | Payload before the prompt | Open Prompt Injection |

## Defense method mapping

| pikit key | Technique | Source |
|---|---|---|
| `delimiters` | Wrap data in XML tags / quotes | Open Prompt Injection |
| `sandwich` | Restate instruction after data | Open Prompt Injection |
| `instructional` | Warn model about data-borne instructions | Open Prompt Injection |
| `spotlighting` | datamarking / encoding / marking | Hines et al., 2024 |
| `random_sequence_enclosure` | Unforgeable random markers | Open Prompt Injection |
| `retokenization` | Token-boundary disruption | Open Prompt Injection |

## Channel mapping

| pikit key | Carrier | Source |
|---|---|---|
| `webpage` | Hidden HTML regions | Greshake et al., 2023 |
| `document` | Document / email body | Greshake et al., 2023 |
| `markdown` | Markdown comments / references | — |
| `code_comment` | Source code comments | — |
| `skills` | Agent Skill files | — |
| `unicode_hidden` | Invisible Unicode characters | — |

## Citation

If you use pikit in your research, please cite:

```bibtex
@misc{pikit,
  title  = {pikit: Prompt Injection Kit},
  author = {pikit contributors},
  year   = {2024},
  url    = {https://github.com/NY1024/pikit},
}
```
