# Voronoi Diagrams using Fortune's Algorithm and Delaunay's Triangulation

## Setup
Intallation of required libraries
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
Then use kernel from Python enviorment with installed dependencies

## Project Structure

This project has the following file structure:

- `delaunay.ipynb`: Notebook presenting the results of Delaunay triangulation and Voronoi diagram
- `fortune.ipynb`: Notebook presenting the implementation of Fortune's algorithm
- `img/`: Directory containing images
- `tests.ipynb`: Time comparison of Fortune's algorithm and Delaunay triangulation
- `voronoi/`: Directory containing the Voronoi diagram implementation
  - `delaunay/`: Directory containing implementation of Voronoi diagram with Delaunay triangulation
    - `delaunay.py`: Implementation of Delaunay triangulation
    - `utils.py`: Helper functions
    - `voronoi.py`: Create Voronoi diagram from Delaunay triangulation
  - `fortune.py`: Main file for Fortune's algorithm
  - `dataStructures.py`: Data structures used in the algorithm
  - `myLL.py`: Implementation of linked list
  - `priorityQueue.py`: Priority queue with removing elements
  - `TInterface.py`: Interface for state structure
  - `utils.py`: Helper functions
  - `visualizer/`: https://github.com/aghbit/Algorytmy-Geometryczne

## Authors

- [Piotr Rzadkowski](https://github.com/ReptilianEye)
- [Olgierd Smyka](https://github.com/OlGierd03)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details