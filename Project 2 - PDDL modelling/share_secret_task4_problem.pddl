;; by Lihua Wang 1164051 
;; 11th April 2021
;; COMP90054-2021-SM1-a2
;; lihuwang@student.unimelb.edu.au

(define (problem task4)
   (:domain secrets)
    (:objects 
        a1 a2 a3 a4 a5 a6 - agent 
        s1 s2 - secret
    )
    (:init
        ;; initial agent a1 knows the secrets s1 and s2
        (knows s1 a1)
        (knows s2 a1)
        
        ;; secret s1, s2 can be told between connected agents in network
        (connected a1 a2)
        (connected a1 a3)
        (connected a2 a4)
        (connected a3 a5)
        (connected a3 a6)
        (connected a4 a5)
        (connected a5 a3)
    )
    (:goal (and
            ;; Goal achieved when agent a5 knows secrets s1 and s2 in a situation that 
            ;; agents a2, a3, a4, a5 can only be told one secret (either s1 or s2)
            (knows s1 a5)
            (knows s2 a5)
            (or (told s1 a2) (told s2 a2))
            (or (told s1 a3) (told s2 a3))
            (or (told s1 a4) (told s2 a4))
            (or (told s1 a6) (told s2 a6))
        )
    )
)
