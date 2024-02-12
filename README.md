![Overview of the reasoning strategy, Figure 3, page 4](https://github.com/Dyke-F/medical-self-discover/blob/main/strategy.png "Overview of the reasoning strategy, Figure 3, page 4")

# Medical Self-Discover
Implementation of the Paper [SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures](https://arxiv.org/pdf/2402.03620v1.pdf) from University of Southern California and Google DeepMind with a focus on improving prompt solution strategies for medical reasoning, especially clinical use cases.

## Install

To install Medical Self-Discover, run the following command in your terminal:


```shell
$ git clone https://github.com/Dyke-F/medical-self-discover.git
```

Make sure to create an .env file with your API key in the root directory.


Alternatively, install from source:
```shell
$ pip install medical-self-discover
```

## Usage

To use Medical Self-Discover, execute the following command with your specified task (type: str) and the path (type: str) where to save the output.

```shell
cd med_self_discover
$ python3 self_discover.py --task "<your task here (str)>" --path "<path/file.json>"
```

## To-Do

- [ ] Collect more and select the best options in MEDICAL_REASONING_MODULES
- [ ] Systematically evaluate strategies
