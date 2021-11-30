;; by Lihua Wang 1164051 
;; 11th April 2021
;; COMP90054-2021-SM1-a2
;; lihuwang@student.unimelb.edu.au

(define (problem task2)
   (:domain secrets)
   (:objects a1 a2 a3 - agent s1 - secret)
   (:init
        ;; initial only agent a1 knows the secret s1
        (knows s1 a1)
        
        ;; secret s1 can be told between connected agents in network
        (connected a1 a2)
        (connected a2 a3)
   )
   (:goal (and
            ;; Goal achieved when agent a3 knows secret s1
            (knows s1 a3)
        )
   )
)
