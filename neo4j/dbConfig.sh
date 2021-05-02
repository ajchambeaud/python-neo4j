#!/bin/bash

sleep 10

echo "[NEO4J dbConfig] Creating constraint for user id"
until cypher-shell -a neo4j 'CREATE CONSTRAINT user_id IF NOT EXISTS ON (n:User) ASSERT n.id IS UNIQUE'
do
  echo "[NEO4J dbConfig] CREATE CONSTRAINT user_id failed. Reatempting in 10 seconds."
  sleep 10
done

echo "[NEO4J dbConfig] Creating constraint for product id"
until cypher-shell -a neo4j 'CREATE CONSTRAINT product_id IF NOT EXISTS ON (n:Product) ASSERT n.id IS UNIQUE'
do
  echo "[NEO4J dbConfig] CREATE CONSTRAINT product_id failed. Reatempting in 10 seconds."
  sleep 10
done
