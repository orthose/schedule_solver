# Les 6 heures de nage
Les « 6 heures de nage » sont une compétition amicale de nage avec palmes 
se déroulant à la piscine d'Étampes. Elle est découpée en 12 relais de 30 minutes 
chacun. Plusieurs équipes s'affrontent afin de réaliser la distance cumulée la 
plus importante. Les bipalmes sont plus fréquemment utilisées mais les monopalmes 
sont également autorisées.

Chaque équipe est donc composée de 12 participants. Chaque participant donne
ses disponibilités, c'est-à-dire les créneaux où il est disponible pour nager
entre 13h00 et 19h00. Le but est de concilier ces disponibilités pour avoir
un seul nageur par créneau. On cherche à maximiser le nombre de nageurs en lice
tout en n'en gardant que 12. Si on a moins de 12 participants, certains devront
nager au moins 2 fois, mais ils risquent d'être moins performants du fait de la 
fatigue. Si on a plus de 12 participants, il faudra faire des choix et en éliminer 
(les éliminés pourront éventuellement intégrer une autre équipe...).

# Modélisation du problème
Pour résoudre ce problème automatiquement on se propose de le modéliser à l'aide
d'un programme d'optimisation sous contraintes en variables entières et plus
précisément binaires.

# Implémentation
Le programme est prototypé en Julia à l'aide des librairies `Cbc` et `JuMP`.
Une autre version en Python sera également réalisée à l'aide de la librairie `PuLP`
et disposera d'une interface graphique client léger utilisant `Flask`.

# Installation & Exécution
## Julia
```shell
$ cd jl/
$ julia
julia> import Pkg
julia> Pkg.add("Cbc")
julia> Pkg.add("JuMP")
$ julia planning.jl
```
