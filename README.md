# ⚫ Blackshield Knight — Sprite Atlas

> *A sworn knight of the obsidian watch. Black heater, iron cross, ember plume, zero retreat.*

The **Blackshield Knight** is the standard-bearer of [Blackshield Company](https://github.com/Blackshield-Company) — the digital mercenary that stands between your data and the dark.

## The Atlas

| Asset | Size | Description |
|---|---|---|
| `spritesheet.png` | 1536×1872 | Full atlas, 8 cols × 9 rows of 192×208 frames |
| `spritesheet.webp` | 1536×1872 | Same atlas, lossless WebP (2.5 KB — the compact field edition) |
| `preview.png` | 1152×1872 | Contact sheet, all 9 states × 6 frames |
| `closeup.png` | 768×832 | The money shot |
| `banner.png` | 3520×688 | Idle row ×3, profile-ready banner on matte black |
| `knight-card.gif` | 2048×2176 | The knight, framed — animated heraldic card: steel ring, dark gradient, idle loop with blade gleam. Built for profile READMEs, display ~500px |

### Animation Rows (6 frames each)

| Row | State |
|---|---|
| 0 | Idle |
| 1 | Running → |
| 2 | Running ← |
| 3 | Waving |
| 4 | Jumping |
| 5 | Failed (dizzy) |
| 6 | Waiting |
| 7 | Running (generic) |
| 8 | Review |

### Palette — the Blackshield livery

| Token | Hex | Use |
|---|---|---|
| `K` | `#1B1F28` | Armor black |
| `S` | `#8FA3BD` | Steel rim |
| `s` | `#DCE5F2` | Bright steel / blade |
| `E` / `e` | `#E07A2F` / `#A04818` | Ember plume |
| `R` / `r` | `#C1121F` / `#6A0C14` | Blood. The iron cross, and the tabard. |
| `B` | `#101014` | Shield field |
| `W` | `#F2F6FC` | Gleam white |

## The Forge

No AI upscaling, no hand-drawn inventory — every frame is generated procedurally:

```bash
python3 gen_blackshield_knight.py
```

The generator (`gen_blackshield_knight.py`) draws the knight on a 96×104 grid, scales it 2× nearest into the 192×208 frame, and bakes the atlas. The shield carries an iron cross: a cross pattée, blood on black, steel-edged, ends bowed in. Running strides, the blade sweeps on the wave row, and the jump leaves the ground. Re-run the script to regenerate every asset.

`pet.json` carries the petdex metadata for the harness that runs it as a desktop companion.

## License

MIT — take the knight, keep the shield polished. See [LICENSE](LICENSE).

---

*Black steel. Iron cross. No scratch, no surrender.* ⚫🛡