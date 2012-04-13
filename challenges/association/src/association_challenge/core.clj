(ns association-challenge.core
  (:gen-class) ;;So that the class is there for the jar
  (:require [clojure.set :as set]))

(def PRODUCTS  '(milk bread chocolate beer soda flour diapers eggs coffee
                 flour butter sausage pasta tomatoes crisps spice cheese
                 chicken beef pork lettuce onion mushroom potatoes rice jam
                 pizza))

(defn create-association-data [three products]
  (repeatedly 10000
              (fn []
                (let [reciept (into #{}
                                    (repeatedly (inc (rand 6))
                                                #(rand-nth products)))
                      intersect (set/intersection reciept (into #{} three))]
                  (if (empty? intersect)
                    reciept
                    (if (< (rand) 0.55)
                      (conj reciept
                            (rand-nth three)
                            (rand-nth three)
                            (rand-nth three))
                      reciept))))))

(defn -main []
  (let [three (repeatedly 3 #(rand-nth PRODUCTS))]
    (println three)
    (doseq [transaction (create-association-data three PRODUCTS)]
      (println (into '()  transaction)))))