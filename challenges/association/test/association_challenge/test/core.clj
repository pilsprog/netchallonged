(ns association-challenge.test.core
  (:use [association-challenge.core])
  (:use [clojure.test]))

(deftest assoctest
  (let [three (rand-nth PRODUCTS)
        assocs (create-association-data three PRODUCTS)
        apri (apriori PRODUCTS assocs 1000)]
    (contains? (into #{} apri) three)))