**Schéma d'architecture**
# Architecture du projet

## Vue d'ensemble

Ce projet implémente une plateforme e-commerce simplifiée en architecture microservices, entièrement conteneurisée avec Docker.

L'application est composée de :

- une **API Gateway Nginx** comme point d'entrée unique
- un microservice **Users**
- un microservice **Products**
- un microservice **Orders**
- une base de données **PostgreSQL dédiée à chaque service**

## Schéma logique

CLIENT (curl / Postman / navigateur)
                │
                ▼
        API Gateway (Nginx) :80
                │
      ┌─────────┼─────────┐
      ▼         ▼         ▼
 Users API   Products API  Orders API
   :5001        :5002        :5003
      │            │            │
      ▼            ▼            ▼
 PostgreSQL    PostgreSQL    PostgreSQL
   Users        Products       Orders