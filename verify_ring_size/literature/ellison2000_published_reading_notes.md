# Ellison (2000) published version: notes from displayed page images only
Source: economics.mit.edu publication node (ProQuest scan, 29 PDF pages, no text layer); PDF page k = journal page 16+k.

## journal p. 30 (PDF 14) - DISPLAYED (p14.png)
- Running head "30 REVIEW OF ECONOMIC STUDIES".
- E(N_x) ~ eps^-(c(x,y)+c(y,Omega)-c(y,x)); W(x,Omega,eps) ~ same, "which is exactly eps^-CR*(Omega)".
- Subtraction of the radius of the intermediate limit set: wait to leave x and probability of y -> Omega "conditional on a transition out of y occurring"; conditional probability approx eps^(c(y,Omega)-c(y,x)) (or eps^(c(y,Omega)-R(y))).
- "4.2. The main theorem". "The following theorem strengthens the result of the previous section by using the modified coradius as the measure of persistence."
- Theorem 2. Let (Z, P, P(eps)) be a model of evolution with noise, and suppose that for some set Omega which is a union of limit sets R(Omega) > CR*(Omega). Then (a) the long-run stochastically stable set of the model is contained in Omega; (b) for any y not in Omega, W(y, Omega, eps) = O(eps^-CR*(Omega)) as eps -> 0.
- Proof: N(A,B,x) = expected number of times states in A occur before the process reaches B, starting at x; Q(A,B,x) = probability A reached before B. Lemma 1 (Appendix): mu^eps(y)/mu^eps(Omega) = N(y,Omega,y) / sum_{omega in Omega} Q(omega, Omega - omega, y) N(Omega, y, omega). Numerator bounded by W(y,Omega,eps); suffices (1) W(y,Omega,eps) = O(eps^-CR*(Omega)) for all y not in Omega and (2) 1/N(Omega,y,omega) = O(eps^R(Omega)) for all omega in Omega. "The second and sixth lemmas in the Appendix contain these two results."
- Last lines: from the second and third lemmas, the radius gives a precise measure of the epsilon-order of the time necessary to leave the ... (continues on p. 31).

## journal p. 23 (PDF 7) - DISPLAYED (p07.png)
- Sect. "3.1. The radius and coradius (and other definitions)". (Z,P) base Markov process of a model of evolution with noise; Omega "a union of one or more of its limit sets".
- Basin: D(Omega) = {z in Z | Prob{exists T s.t. z_t in Omega for all t > T | z_0 = z} = 1} (unperturbed process converges to Omega with probability one).
- Path from X to Y: "a finite sequence of distinct states (z1, z2, ..., zT) with z1 in X, z_t not in Y for 2 <= t <= T-1, and zT in Y". S(X,Y) = set of all paths. c(path) = sum_{t=1}^{T-1} c(z_t, z_t+1).
- Radius: "the minimum cost of any path from Omega out of D(Omega)": R(Omega) = min over S(Omega, Z - D(Omega)) of c(path). With C(X,Y) = min over S(X,Y): R(Omega) = C(Omega, Z - D(Omega)).
- In each example c(x,y) = min_{z | P_xz(0)>0} d(z,y), d satisfying the triangle inequality (footnote 8: unperturbed dynamics then mutations). Method to prove R(Omega) = k: exhibit w in Omega, z2 not in D(Omega) with c(w,z2) = k, and show two conditions (footnote 9: least costly path is a direct path).
## journal p. 24 (PDF 8) - DISPLAYED (p08.png)
- Coradius: CR(Omega) = max_{x not in Omega} min_{path in S(x,Omega)} c(path). Maximum always achieved at a state which belongs to a limit set. Equivalent: max_{x not in D(Omega)} min_{path in S(x, D(Omega))}.
- "3.2. The theorem". Theorem 1. Let (Z,P,P(eps)) be a model of evolution with noise, and suppose that for some set Omega which is a union of limit sets R(Omega) > CR(Omega). Then: (a) the long-run stochastically stable set of the model is contained in Omega; (b) for any y not in Omega, W(y,Omega,eps) = O(eps^-CR(Omega)) as eps -> 0.
- O-notation defined: exists C, xbar > 0 with |f(x)| < C|g(x)| on (0, xbar). "Theorem 1 is a special case of Theorem 2, and therefore a formal proof is omitted."
- Informal argument: time in D(Omega) bounded below by k1 eps^-R(Omega); time outside bounded above by k2 eps^-CR(Omega).
- "3.3. Examples" begins.

## journal p. 28 (PDF 12) - DISPLAYED (p12.png)
- Top: end of proof of a corollary (CR(A) <= q(N-1)+1; "R(A) > CR(A) and Theorem 1 applies").
- Heading "4. STEP-BY-STEP EVOLUTION AND AN IMPROVED THEOREM": "a more powerful theorem is obtained by deriving a tighter bound on the time required for evolution toward a limit set"; "using a measure I call the modified coradius"; large changes occur more quickly "by passing through a number of intermediate steady states".
- "4.1. The modified coradius": Omega a union of limit sets, (z1..zT) a path from x to Omega; L1, L2, ..., Lr subset Omega [as printed] the sequence of limit sets through which the path passes consecutively (a limit set can appear multiple times but not successively). x may be an element of L1; L_i not subset of Omega for i < r.
- Modified cost function c*: "by subtracting from the cost of the path the radius of the intermediate limit sets through which the path passes": c*(z1..zT) = c(z1..zT) - sum_{i=2}^{r-1} R(L_i).
## journal p. 29 (PDF 13) - DISPLAYED (p13.png)
- "(Note that R(L1) is not included in the sum.)"; c*(x,Omega) = min over S(x,Omega) of c*(path).
- "The modified coradius of the basin of attraction of Omega is then defined by CR*(Omega) = max_{x not in Omega} c*(x,Omega)." "Note that CR*(Omega) <= CR(Omega)."
- Diagram: left x->w at eps^3: cost 3, expected wait 1/eps^3; right x->y->z->w, each eps: cost 3, expected wait 3/eps. "the modified coradius of w is indeed three in the process on the left and one in the process on the right".
- Three-state process x<->y->Omega: Omega always the unique LRSS state because R(Omega) = infinity; if c(x,y) > c(y,x) and c(y,Omega) > c(y,x) then CR*(Omega) = c(x,y) + c(y,Omega) - c(y,x); W(x,Omega,eps) = E(N_x) + E(N_y).

## journal p. 17 (PDF 1) - DISPLAYED (p01.png)
- Header: "Review of Economic Studies (2000) 67, 17-45"; "0034-6527/00/00020017$02.00"; "(c) 2000 The Review of Economic Studies Limited". Title "Basins of Attraction, Long-Run Stochastic Stability, and the Speed of Step-by-Step Evolution"; GLENN ELLISON, Massachusetts Institute of Technology. "First version received September 1995; final version accepted February 1999 (Eds.)".
- Abstract: two observations (LRSS related to speed of evolution toward and away; evolution more rapid via "a series of small steps between intermediate steady states"); "two new measures, the radius and modified coradius, to characterize the long run stochastically stable set ... and to bound the speed"; "Though not universally powerful"; applications: 1/2-dominant equilibria, two-dimensional local interaction, "cycles as long run stochastically stable sets".
- No DOI printed on the page. (pypdf text of the ProQuest cover line: "The Review of Economic Studies; Jan 2000; 67, 230; ABI/INFORM Global pg. 17".)
## journal p. 31 (PDF 15) - DISPLAYED (p15.png)
- "Lemmas 2 and 3 imply that W(l, Z - D(L), eps) ~ eps^-R(L) for any state l belonging to a limit set L."
- "the main theorem of this paper is not universally applicable"; gives "a bound on the convergence rate as well as a long-run limit"; "radius-modified coradius theorem may be easier to apply".
- Footnote 17: "In Section 6.3 it is shown that whenever Theorem 2 applies to a single limit set Omega the long run stochastically stable set could have been found by applying 'tree surgery' arguments in a fairly systematic way."
- "4.3. Examples"; Example 2 (3x3 game, uniform matching, mu*(B) = 1 for N sufficiently large).

## journal p. 20 (PDF 4) - DISPLAYED (p04.png)
- "An alternate proof of the long run stochastic stability part of the main theorem based on a Freidlin-Wentzell 'tree surgery' argument is also given" (builds on Young 1993a, Kandori-Rob 1995, Ellison 1993, Evans 1993, Samuelson 1994).
- "2. MODEL AND DEFINITIONS", 2.1. Definition 1: model of evolution with noise = triple (Z, P, P(eps)): 1. finite set Z (state space); 2. Markov transition matrix P on Z; 3. family P(eps), eps in [0, eps-bar): (i) P(eps) ergodic for each eps > 0; (ii) continuous in eps with P(0) = P; (iii) a (possibly asymmetric) cost function c: Z x Z -> R+ u {infinity} such that lim_{eps->0} P_zz'(eps)/eps^c(z,z') exists and is strictly positive if c(z,z') < infinity (P_zz'(eps) = 0 for small eps if c = infinity).
- (Z,P) = base or unperturbed Markov process.
## journal p. 36 (PDF 20) - DISPLAYED (p20.png)
- "6. RELATIONSHIPS WITH THE LITERATURE"; 6.1 Applications: theorem applicable to almost every model for which the LRSS set has previously been identified (KMR 1993, Ellison 1993, Evans 1993, Noldeke-Samuelson 1993, 1997, Robson-Vega-Redondo 1996, Samuelson 1994, Young 1993a,b).
- Footnote 21: "The results of the Samuelson and Noldeke-Samuelson analyses are most easily rederived by showing that their lemmas follow from a modified coradius computation."
## journal p. 37 (PDF 21) - DISPLAYED (p21.png)
- "6.2. Relationships with other papers". R(Omega) > CR(Omega) as a sufficient condition "was independently given by Evans (1993) (see Lemma 3.1)", tree surgery argument in the proof of Theorem 1 of Ellison (1993).
- KEY: intermediate steady states speeding evolution "plays a prominent role in the work of Samuelson (1994) and Noldeke and Samuelson (1993, 1997). In those papers, the long-run stochastically stable set is identified using a lemma which (in my words) states that a component Omega of limit sets receives probability one in the limit distribution if R(Omega) > 2 [to be checked by zoom] and Omega can be reached from any other limit set via a chain of single mutations (a condition which ensures" (continues p. 38).

## p. 37 zoom (p21_zoom.png) - DISPLAYED: the scan reads "if R(Omega) > 2 and Omega can be reached from any other limit set via a chain of single mutations (a condition which ensures" [the relation sign reads as ">" in the scan; "≥" cannot be excluded at this resolution].
## journal p. 38 (PDF 22) - DISPLAYED (p22.png)
- continues: "that CR*(Omega) = 1). This paper adds to this lemma the idea that a path deserves 'credit' for R(L) mutations (rather than one) when passing through the limit set L and combines it with the previous one so that it can be applied in models where the nonselected limit sets are not so unstable as to be upset by just a single mutation."
- Waiting times: "the waiting time to reach a long-run stochastically stable state Omega which satisfies R(Omega) > CR(Omega) is at most O(eps^-CR(Omega))" (generalising Binmore-Samuelson 1997, Robson-Vega-Redondo 1996).
- "6.3. A Freidlin-Wentzell 'tree surgery' argument". Theorem 3. Let (Z,P,P(eps)) be a model of evolution with noise. If for some limit set Omega and some state x not in Omega we have R(Omega) > c*(x,Omega) then mu*(x) = 0. If R(Omega) = c*(x,Omega) then mu*(x) > 0 implies mu*(Omega) > 0.
- "unlike Theorems 1 and 2, the Omega in the statement of this proposition is required to be a single limit set rather than a union of limit sets. When Omega is a single limit set, part (a) of Theorem 2 follows from the first conclusion of Theorem 3 ... implies that mu*(Omega) = 1."
- Proof: x-tree t: Z -> Z, cost c(t) = sum_{z != x} c(z,t(z)); LRSS states correspond to minimum cost trees (Freidlin-Wentzell).
## journal p. 39 (PDF 23) - DISPLAYED (p23.png)
- Proof of Theorem 3 continued (limit sets L1..Lr = Omega crossed along the path, may be assumed distinct; construct w-tree t''; c(t'') - c(t') <= c*(x,Omega) + sum R(L_i) - (R(Omega) + sum R(L_i)) < 0). "7. CONCLUSION" begins.

## journal p. 22 (PDF 6) - DISPLAYED (p06.png)
- limit distribution mu* = lim_{eps->0} mu^eps; a state z is long-run stochastically stable if mu*(z) > 0.
- LRSS set contained in the recurrent classes of (Z,P) (Young 1993a); recurrent classes = "limit sets"; may be steady states, cycles, or collections of states between which the system shifts randomly.
- W(x,Y,eps) = expected wait until a state in Y is first reached from x in the eps-perturbed model; convergence speed via max_x W(x,Omega,eps).
- "3. A SIMPLE RADIUS-CORADIUS THEOREM" begins.
## journal p. 25 (PDF 9) - DISPLAYED (p09.png)
- Example 1: N players, uniform matching, best-reply dynamics with independent trembles. Left game: mu*(A) = 1 for N large. Right game: mu*(B) = mu*(C) = 1/2: the LRSS set is the cycle alternating between all-B and all-C.
- Proof via R(A) > CR(A), Theorem 1.
## journal p. 26 (PDF 10) - DISPLAYED (p10.png)
- cycle {B,C} is a limit set; R({B,C}) approx (3/7)N, CR({B,C}) approx (1/4)N; "For N large Theorem 1 gives mu*({B,C}) = 1, and the result follows by symmetry."
- "A variety of learning and evolutionary models have cycles as limit sets."
- "3.4. An application: generalizing risk dominance to 1/2-dominance" begins.
## journal p. 37 confirmation from the working paper (rendered crop of WP PDF page 32, printed p. 30, wp_p30_lemma.png - DISPLAYED): same sentence, reads "if R(Omega) > 2 and Omega can be reached from any other limit set via a chain of single mutations (a condition which ensures that CR*(Omega) = 1.)"
