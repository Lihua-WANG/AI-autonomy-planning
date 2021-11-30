;; by Lihua Wang 1164051 
;; 11th April 2021
;; COMP90054-2021-SM1-a2
;; lihuwang@student.unimelb.edu.au

(define (problem task3)
    (:domain secrets)
    (:objects 
        a1 a2 a3 a4 a5 a6 - agent 
        s1 s2 - secret
    )
    (:init
        ;; initial only agent a1 knows the secret s1 and agent a2 knows secret s2
        (knows s1 a1)
        (knows s2 a2)
        
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
            ;; Goal achieved when agent a5 knows secret s1 and agent a6 knows secret s2
            (knows s1 a5)
            (knows s2 a6)
        )
   )
)
