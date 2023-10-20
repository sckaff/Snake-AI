# Snake AI

```
python agent.py
```

Requirements: ipython, matplotlib, numpy, pygame, torch
```
pip install -r requirements.txt
```

### In progress

- [ ] Allow snake to cross the wall, and make change optional.
- [ ] Make the snake's own body a collision.
- [ ] Improve discount rate, learning rate, optimization function, loss function, so the snake to learns more efficiently and successfully complete the game in a reasonable time.
    - Current architecture 11x256x3 (ReLU).
- [ ] Load saved model after opening snake-ai, and save best model for demo.

### OBS
- Change the speed of the game on "game.py" </br>
- Its problem is not avoiding itself. Must improve architecture, or change physics.
