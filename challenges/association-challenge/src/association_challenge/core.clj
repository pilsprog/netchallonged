(ns association-challenge.core
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

(defn apriori [products reciepts support]
  (letfn [(f [prods]
            (for [product prods
                  :when (< support
                           (count (filter #(set/superset? % product)
                                                  reciepts)))]
              product))]
    (loop [candidates (map hash-set products)
           rules []]
      (if (empty? candidates)
        rules
        (let [cs (f candidates)
              rs (f (distinct
                     (mapcat #(for [c (into [] (reduce set/union cs))
                                    :when (not (contains? % c))]
                                (conj % c))
                             cs)))]
          (recur rs
                 (concat rules rs)))))))

(defn -main []
  (let [three (repeatedly 3 #(rand-nth bPRODUCTS))]
    (println three)
    (doseq [transaction (create-association-data three PRODUCTS)]
      (println (into '()  transaction)))))