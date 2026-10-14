# Introducing the Open Knowledge Format

> Source: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
> Collected: 2026-10-14
> Published: 2026-06-12
> Authors: Sam McVeety, Amir Hormati

## Overview

As foundation models continue to improve, the lack of relevant context often limits what they can do, especially as they are used to build agentic systems. While these models can help you write code, summarize documents, or analyze a dataset, they still need the right information to produce accurate and actionable results.

That's why today, we're introducing the Open Knowledge Format (OKF), an open specification that formalizes the LLM-wiki pattern into a portable, interoperable format. This is a vendor-neutral, agent- and human-friendly standard for representing the metadata, context, and curated knowledge that modern AI systems need.

As published, OKF v0.1 represents knowledge as a directory of markdown files with YAML frontmatter, with a small set of agreed-upon conventions that let wikis written by different producers be consumed by different agents without translation.

That's it. No complex compression scheme, no new runtime, no required SDK. A bundle of OKF documents is:
- Just markdown: readable in any editor, renderable on GitHub, indexable by any search tool
- Just files: shippable as a tarball, hostable in any git repo, mountable on any filesystem
- Just YAML frontmatter: for the small set of structured fields that need to be queryable: type, title, description, resource, tags, and timestamp

## Knowledge as a Living Wiki

Developer teams are changing how they build AI agents. Instead of using models to search the same documents for the same facts over and over, you can give your agents a shared markdown library that grows more useful over time. This lets your agents take on the drudgery of reading and updating their own files, while your team curates the content and manages it like code.

Andrej Karpathy, the prominent AI researcher and educator, articulates this idea most crisply in his LLM Wiki gist. "LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass," he writes. The bookkeeping that causes humans to abandon personal wikis is exactly what LLMs are good at.

Similar knowledge-as-Wiki pattern keeps reappearing under different names: Obsidian vaults wired to coding agents, the AGENTS.md / CLAUDE.md family of convention files, repos full of index.md and log.md artifacts that agents consult before doing real work, and metadata as code repositories inside data teams.

The pattern is compelling and powerful, but each instance is bespoke. Karpathy's wiki and your team's wiki and a vendor's catalog export may all look alike (markdown, frontmatter, cross-links), but none of them are intentionally designed to cooperate. There is no agreed-upon answer to what fields every document should carry, or what filenames mean what. As a result, the knowledge encoded in wikis remains siloed within the original teams, leading to redundant effort whenever a new agent is built.

## What OKF Provides

The answer to this problem isn't another knowledge service. You need a format, a way to represent knowledge that:
- Anyone can produce, without an SDK
- Anyone can consume, without an integration
- Survives moving between systems, organizations, and tools
- Lives in version control alongside the code it describes
- Is readable by humans and parseable by agents: the same file, no translation layer

By design, OKF is that format.

## How OKF Works: Directory and Concept Specification

An OKF bundle is a directory of markdown files representing concepts: anything you want to capture, including tables, datasets, metrics, playbooks, runbooks, and APIs. Each concept is one file. The file path is the concept's identity:

```text
sales/
├── index.md
├── datasets/
│   ├── index.md
│   └── orders_db.md
├── tables/
│   ├── index.md
│   ├── orders.md
│   └── customers.md
└── metrics/
    ├── index.md
    └── weekly_active_users.md
```

Each concept document has a small block of YAML frontmatter for structured fields and a markdown body for everything else:

```yaml
---
type: BigQuery Table
title: Orders
description: One row per completed customer order.
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=orders
tags: [sales, revenue]
timestamp: 2026-05-28T14:30:00Z
---
```

Concepts link to each other with normal markdown links, turning the directory into a graph of relationships that is richer than the parent/child links implied by the file system. Bundles can optionally include index.md files (for progressive disclosure as agents navigate the hierarchy) and log.md files (for chronological history of changes).

## Three Principles Behind the Design

1. Minimally opinionated: OKF requires exactly one thing of every concept: a type field. Everything else (what types exist, what other fields to include, what sections the body has) is left to the producer. The spec defines the interoperability surface, not the content model.
2. Producer/consumer independence: OKF cleanly separates who writes the knowledge from who consumes it. A bundle hand-authored by a human can be consumed by an AI agent. A bundle generated by a metadata export pipeline can be browsed in a visualizer. A bundle synthesized by one LLM can be queried by another. The format is the contract; the tooling at each end is independently swappable.
3. Format, not platform: OKF is not tied to any specific cloud, database, model provider, or agent framework. It will never require a proprietary account or SDK to read, write, or serve.

