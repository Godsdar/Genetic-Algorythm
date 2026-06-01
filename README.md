# Genetic Algorithm Visualizer

A desktop application that visualizes how a genetic algorithm solves 
a pathfinding problem — guiding agents toward a target while avoiding obstacles.

## How it works

Agents (individuals) evolve over generations using crossover and mutation 
to find optimal paths on a grid. Each generation is rendered in real time 
using Tkinter.

## Features

- Interactive grid — place obstacles and target manually or generate randomly
- Real-time visualization of each generation
- Skip ahead multiple generations if convergence is slow
- Configurable parameters: population size, crossover/mutation probability, 
  max generations

## Tech stack

Python, Tkinter

## Run

```bash
python main.py
```

## Parameters (main.py)

| Parameter | Default |
|---|---|
| Population size | 50 |
| Crossover probability | 0.9 |
| Mutation probability | 0.1 |
| Max generations | 100 |
| Grid size | 20×11 |
