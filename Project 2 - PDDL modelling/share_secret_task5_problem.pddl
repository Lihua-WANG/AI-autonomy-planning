;; by Lihua Wang 1164051 
;; 11th April 2021
;; COMP90054-2021-SM1-a2
;; lihuwang@student.unimelb.edu.au

(define (problem task5)
   (:domain secrets)
    (:objects 
        a1 a2 a3 a4 a5 a6 - agent 
        s1 s2 - secret
    )
    (:init
        ;; secret s1, s2 can be told between connected agents in network
        (connected a1 a2)
        (connected a1 a3)
        (connected a2 a4)
        (connected a3 a5)
        (connected a3 a6)
        (connected a4 a5)
        (connected a5 a3)

        ;; initial agent a1 believes secret s1 is true
        (belief_true a1 s1)
        
        ;; initial agent a5 is a deceiver
        (deceiver a5)
    )
    (:goal (and
            ;; Goal achieved when agent a6 believes secret s1 is true
            ;; and agent a3 believes scret s1 is false
            (belief_true a6 s1)
            (belief_false a3 s1)
        )
    )
)
