# PREVIEW: Weekly digest 2026-W42 (off-schedule test run)

> **This is a preview, not the Sunday advisory.** It was run on Friday Oct 16 at the user's request so they
> could see the format. No calls were logged to `journal/decisions.jsonl`, the scorecard will not grade it, and
> `reports/latest.md` was not touched. The real run on Sunday 08:07 HKT writes `weekly/2026-W42/digest.md` from
> a fresh build and may differ.

## Summary
- Regime: **risk-off**. The CSI 300 is -11.01% below its 200-day average and down -12.97% over 12 weeks; only
  15.7% of tracked funds are above their 200-day average.
- Portfolio vs target vs benchmark: no holdings yet (`portfolio/holdings.yaml` is empty), so there is no
  portfolio return to compare with the 12%/yr target or the CSI 300. The scorecard has no graded calls yet.
- No call clears the 60% confidence floor this week, so every call below is **Watch**. Nothing here is a Buy.
- If you want to start positions anyway, the mechanical default is the rules-only core sleeve: 511010 bonds at
  25.0%, 510880 dividend at 16.3%, 510300 CSI 300 at 15.4%, 518880 gold at 13.3%, with 30.0% left unallocated.
  Most of that sleeve moves as one defensive bet (cluster 012111).
- Every growth theme on the watchlist (AI, chips, robotics, space, materials) is deep in drawdown with no
  sign of turning yet; healthcare and power are holding up best.

## Holdings: top 3
_No holdings. Add your positions to `portfolio/holdings.yaml` (code, units, cost, date bought) and the Sunday
run will give each one a Buy or Sell with a percentage._

## Theme watchlist
p_up = the chance the fund beats the CSI 300 over the next 4 weeks. Each starts from its composite band's base
rate (20-40: 47.6%, 40-60: 48.7%, 60-80: 51.1%), then moves a few points for named reasons.

### AI and compute (growth)
News is heavy but negative: a global AI selloff and US chip stocks opening sharply lower on Oct 15. 30 new
products launched in 6 months, a launch wave, which is a crowding warning.

| code | name | call | % | reason |
|---|---|---|---|---|
| 159819 | 人工智能ETF易方达 | Watch | 42% | base 49%; risk-off, AI selloff news and the launch wave each take points off; -28.78% over 12 weeks |
| 515880 | 通信ETF国泰 | Watch | 41% | base 48%; same three penalties; -44.66% off its 52-week high, the weakest in the theme |
| 159852 | 软件ETF嘉实 | Watch | 43% | base 48%; software fell less than hardware (-9.09% over 12 weeks), still below its 200-day average |

### Semiconductors and equipment (growth)
19 news mentions, mostly the US chip selloff. 159516, 588170 and 588710 are back above their 200-day
averages, the only growth products that are.

| code | name | call | % | reason |
|---|---|---|---|---|
| 159516 | 半导体设备ETF国泰 | Watch | 45% | base 49% (composite 50.9); risk-off and the chip selloff; above its 200-day average |
| 588170 | 科创半导体ETF华夏 | Watch | 44% | base 49%; same penalties; above its 200-day average, -25.31% over 12 weeks |
| 588200 | 科创芯片ETF嘉实 | Watch | 43% | base 49%; same penalties, plus still below its 200-day average |

All three are one cluster (159516): one bet, not three.

### Robotics and embodied AI (growth)
Only 2 news mentions; no launch wave.

| code | name | call | % | reason |
|---|---|---|---|---|
| 159530 | 机器人ETF易方达 | Watch | 46% | base 49%; risk-off; -37.89% off its 52-week high |
| 159667 | 工业母机ETF国泰 | Watch | 46% | base 49%; risk-off; -31.33% over 12 weeks |
| 159663 | 机床ETF华夏 | Watch | 45% | base 48%; risk-off; very thin turnover |

### Commercial aerospace and satellites (emerging)
5 news mentions; 4 launches in 6 months, not yet a wave.

| code | name | call | % | reason |
|---|---|---|---|---|
| 159206 | 卫星ETF永赢 | Watch | 45% | base 48%; risk-off; -47.75% off its 52-week high |
| 159227 | 航空航天ETF华夏 | Watch | 45% | base 48%; risk-off; fell less over 12 weeks (-5.83%) |
| 159267 | 航天ETF华安 | Watch | 44% | base 48%; risk-off; single issuer, thin turnover |

### Innovative drugs and biomedicine (growth)
5 news mentions, nothing material. Healthcare has been one of the steadier corners: down only modestly over
4 weeks while the broad market fell.

| code | name | call | % | reason |
|---|---|---|---|---|
| 159883 | 医疗器械ETF永赢 | Watch | 47% | base 49% (composite 49.4); a small risk-off cut, smaller than for growth themes |
| 159992 | 创新药ETF银华 | Watch | 47% | base 49%; same; -11.18% over 12 weeks, -16.49% off its high |
| 159859 | 生物医药ETF天弘 | Watch | 46% | base 49%; same, less liquid |

### Grid equipment and power (growth)
4 news mentions. 15 launches in 6 months is a launch wave. Power utilities sit in the defensive cluster.

| code | name | call | % | reason |
|---|---|---|---|---|
| 159611 | 电力ETF广发 | Watch | 49% | base 51% (composite 61.3); launch wave; no risk-off cut because utilities are defensive |
| 159625 | 绿色电力ETF嘉实 | Watch | 47% | base 49%; launch wave; same cluster as 159611 and thin turnover |
| 159326 | 电网设备ETF华夏 | Watch | 44% | base 49%; risk-off and launch wave; -36.58% off its 52-week high |

### New materials and rare earths (emerging)
1 news mention.

| code | name | call | % | reason |
|---|---|---|---|---|
| 516150 | 稀土ETF嘉实 | Watch | 46% | base 49%; risk-off; -37.58% off its 52-week high |
| 562800 | 稀有金属ETF嘉实 | Watch | 46% | base 49%; risk-off; same cluster as 516150 |
| 588160 | 科创新材料ETF南方 | Watch | 45% | base 48% (composite 28.3); risk-off; moves with the chip cluster |

## New picks
### 012111 鹏华安颐混合A: Watch 55%
- Cluster 012111. Highest composite this week (94.8); base 55% (band 80-100), no adjustment. Low volatility
  (6.13% annualised) and only -3.65% max drawdown over 52 weeks.
- Fits as a low-risk mixed fund while equities are risk-off. It is an open-end fund, so selling within 7 days
  usually costs a redemption penalty.
- Falsifier: its NAV breaks its 52-week drawdown low, or the regime turns risk-on and equities lead.

### 510880 红利ETF华泰柏瑞: Watch 54%
- Cluster 012111. Composite 75.4; base 51% (band 60-80), plus a few points because dividend stocks are
  defensive in risk-off. It is +6.94% over 12 weeks and only -2.66% off its 52-week high. A rules-only core buy
  at 16.3%.
- Same cluster as 012111, 511010 and 512800 (银行, composite 70.5): pick one of them, not several.
- Falsifier: banks and dividend names start falling with the market, or rate cuts at the Oct 20 LPR shift
  money into growth.

### 511010 国债ETF国泰: Watch 52%
- Cluster 012111. Composite 75.8; base 51%, plus a little for the PBOC's easing tone (net injection, "moderately
  loose" policy restated on Oct 15), minus a little for the **turnover surge** crowded flag. Crowded means no buy
  this week even though it is the largest rules-only core weight (25.0%).
- Falsifier: bond yields rise on US inflation (US CPI and PPI both came in hot) or heavy new treasury supply.

## Risks and what would change my mind
- Oct 19: China Q3 GDP and September activity data, plus the Financial Street Forum, where "major policy" is
  expected. A strong stimulus package would be the main reason to lift growth themes off Watch.
- Oct 20: the LPR. A cut would help banks less and growth more.
- Oct 20–21: Nvidia GTC Berlin. A good reception could steady AI and chip ETFs; another leg down would confirm
  the selloff.
- Hot US inflation (CPI 3.7%, PPI higher) keeps global risk appetite weak.
- What changes my mind: breadth back above half of funds, or the CSI 300 back above its 200-day average.

## Data notes
- Data as of 2026-10-15 close; fact sheet built 2026-10-16 00:58 HKT.
- Eastmoney's ETF and LOF feeds are down from GitHub, so ETF premium/discount and 5-day share changes are
  blank; Sina is filling ETF prices.
- News collection started Oct 15, so last week has almost nothing to compare against, and only one daily
  digest (Oct 14) exists.
- The signal backtest finds no signal proven yet (all "unproven" or "rejected"), so the composite spreads
  between bands are small; treat every percentage as close to a coin flip.
- This is a preview: nothing was logged or graded.

Research signals from public data, not financial advice.
