;; by Lihua Wang 1164051 
;; 11th April 2021
;; COMP90054-2021-SM1-a2
;; lihuwang@student.unimelb.edu.au

(define 
    (domain secrets)
    (:requirements :strips :typing :equality :adl)
    (:types agent secret)

    (:predicates
        ;; one agent knows one secret
        (knows ?s - secret ?a - agent)
        ;; two agents connected in the nestwork that
        ;; one can send secret and the othet can recieve secret 
        (connected ?as ?ar - agent)
        ;; one secret has ever visisted one agent 
        (told ?s - secret ?a - agent)
        
        ;; the true flag shows that one agent belief one secret is true
        (belief_true ?a - agent ?s - secret)
        ;; the false flag shows that one agent belief one secret is false
        (belief_false ?a - agent ?s - secret)
        ;; one agent deceiver the secret
        (deceiver ?a - agent)
    )
    
    (:action tell
        :parameters (?s - secret ?as ?ar - agent)
        ;; a sent agent should know the secret,
        ;; one sent agent can only tell a secret to recieve agent if they are connected on the network.
        ;; a receive agent doesn't know the secret before the secret was told to it
        :precondition (and
            (knows ?s ?as)
            (connected ?as ?ar)
            (not (told ?s ?ar))
        )
        ;; once a receieve agent recieved the secret, it will know the secret,
        ;; and flag the recieve agent has been told the secret
        :effect (and
            (knows ?s ?ar)
            (told ?s ?ar)
        )
    )   
    
    (:action share_belief
        :parameters (?s - secret ?as ?ar - agent)
        ;; two agents can only share belief if they are connected on the network
        ;; one sent agent should believe one secret is true or false
        :precondition (and
            (connected ?as ?ar)
            (or (belief_true ?as ?s) (belief_false ?as ?s))
        )
        ;; if the send agent is a deceiver, 
        ;; the secret belief of a recieve agent will be opposite to send agent
        ;; if the send agent is not a deceiver,
        ;; the the secret belief of a recieve agent will be the same as send agent
        :effect (and
            (when (and (deceiver ?as) (belief_true ?as ?s))
                (and (belief_false ?ar ?s)))
            (when (and (deceiver ?as) (belief_false ?as ?s))
                (and (belief_true ?ar ?s)))
            (when (and (not (deceiver ?as)) (belief_true ?as ?s))
                (and (belief_true ?ar ?s)))
            (when (and (not (deceiver ?as)) (belief_false ?as ?s))
                (and (belief_false ?ar ?s)))
        )
    )
)
