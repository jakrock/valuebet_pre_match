#!/bin/bash

# Commandes à exécuter en parallèle
commands=(
  "nohup /home/romualdjja/projet1/projet1/comparateur_live/executor.py >/dev/null 2>&1 &"
  "nohup /home/romualdjja/projet1/projet1/comparateur_live/modelll.py >/dev/null 2>&1 &"
  "nohup /home/romualdjja/projet1/projet1/comparateur_live/model1111.py >/dev/null 2>&1 &"
  "nohup /home/romualdjja/projet1/projet1/fast_api/fast.py >/dev/null 2>&1 &"
)

# Boucle pour exécuter les commandes en arrière-plan
for cmd in "${commands[@]}"; do
  eval "$cmd"
  echo "Commande exécutée en arrière-plan: $cmd"
done

echo "Toutes les commandes ont été lancées en arrière-plan."
