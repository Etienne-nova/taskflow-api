# Notes de sécurité — Projet 1

## Vulnérabilité résiduelle acceptée (scan Trivy)

Après mise à jour de Django (5.2.13) et sqlparse (0.6.0), la seule
vulnérabilité CRITICAL restante concerne `perl-base` (CVE-2026-13221),
un paquet système Debian sans correctif amont disponible à ce jour
(statut "affected").

Ce paquet n'est jamais invoqué par le code applicatif Django — Perl n'est
utilisé par aucune fonctionnalité de l'API. Le risque d'exploitation réel
est jugé négligeable dans ce contexte, et sera réévalué au prochain
rescan Trivy (intégré au pipeline CI/CD du Projet 2).

## Dette technique assumée

- Les serializers Project/Task ne séparent pas lecture/écriture (EX-12).
  Aucune donnée sensible n'est exposée dans les faits, mais la séparation
  formelle demandée par le cahier des charges n'est pas implémentée.
- `notify_task_assignment` se déclenche à chaque mise à jour d'une tâche
  tant qu'un `assigned_to` existe, pas uniquement lors d'un changement
  réel d'assignation.
