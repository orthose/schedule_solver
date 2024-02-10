# :author: Maxime VINCENT

#=
$ julia
julia> import Pkg
julia> Pkg.add("Cbc")
julia> Pkg.add("JuMP")
$ julia planning.jl 
=#

using Cbc, JuMP

# TODO: Encapsuler dans une fonction

# Disponibilités des nageurs de 13h00 à 18h30
A = [
    1 1 0 1 0 0 0 0 1 1 1 1; # Nageur 1
    1 1 0 0 1 1 1 0 0 1 1 1;
    1 1 0 0 0 0 1 1 1 0 0 1;
    1 1 1 1 1 1 1 1 1 1 1 1;
    1 1 0 1 0 1 1 1 1 0 1 1;
    1 1 0 0 0 0 0 0 0 0 0 0;
    0 1 1 1 1 0 0 0 1 0 0 0;
    0 1 1 1 1 1 1 0 1 1 1 1;
    0 1 0 1 0 0 1 0 1 1 1 1;
    0 1 1 0 1 0 1 0 1 1 1 1;
    0 1 1 1 1 1 0 0 0 1 1 1;
    0 0 0 1 1 1 1 1 0 0 1 1; # Nageur 12
]

n_swims = size(A, 1) # Nombre de nageurs
n_slots = size(A, 2) # Nombre de créneaux
max_slots = 1 # Nombre maximum de créneaux autorisé par nageur 

m = JuMP.Model(Cbc.Optimizer)

# Si x[i,j] = 1 alors le nageur i est inscrit au créneau j
@variable(m, x[i in 1:n_swims, j in 1:n_slots], Bin)

# Chaque nageur ne doit être inscrit que sur max_slots créneau(x) au plus
@constraint(m, line[i in 1:n_swims], sum(x[i,j] for j in 1:n_slots) <= max_slots)

# Un créneau ne peut être accordé au plus qu'à un seul nageur
@constraint(m, column[j in 1:n_slots], sum(x[i,j] for i in 1:n_swims) <= 1)

# Si le nageur i n'est pas disponible sur le créneau j 
# on ne doit pas lui proposer ce créneau
@constraint(m, available[i in 1:n_swims, j in 1:n_slots ; A[i,j] == 0], x[i,j] == 0)

# Une équipe est composée au maximum de n_slots nageurs
# puisqu'on doit avoir au plus un nageur par créneau
# Contrainte redondante avec column conjuguée à la fonction objectif
#@constraint(m, team, sum(x[i,j] for i in 1:n_swims, j in 1:n_slots) <= n_slots)

# On cherche à maximiser le nombre de nageurs en lice car faire nager 
# plusieurs fois un même nageur risque de lui faire perdre en performance
# et plus on est de fous plus on rit !
@objective(m, Max, sum(x[i,j] for i in 1:n_swims, j in 1:n_slots))

MOI.set(m, MOI.Silent(), true)
optimize!(m)
is_optimal = termination_status(m) == MOI.OPTIMAL

if is_optimal println("Le pb a été résolu à l'optimum")
else println("Le pb n'a pas été résolu à l'optimum")
end

println("sum(x[i,j]) = ", round(Int, JuMP.objective_value(m)))

for i in 1:n_swims
    for j in 1:n_slots
        if (round(Int, JuMP.value(x[i,j])) == 1)
            println("Nageur ", i, " nage en position ", j)
            break
        end
    end
end
