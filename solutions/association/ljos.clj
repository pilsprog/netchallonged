(ns association-challenge.solution
  (:require [clojure.set :as set]))

(defn apriori [products transactions support]
  (letfn [(f [products]
            (for [product products
                  :when (< support
                           (count (filter (partial set/subset? product)
                                          transactions)))]
              product))
          (g [cs]
            (f (distinct
                (mapcat #(for [c (reduce set/union cs)
                               :when (not (contains? % c))]
                           (conj % c))
                        cs))))]
    (apply concat
           (take-while (complement empty?)
                 (reductions (fn [l _] ((comp g f) l))
                             ((comp g f map) hash-set products)
                             (range))))))
