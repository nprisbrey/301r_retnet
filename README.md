# Are You Using Retentive Networks? (RetNets) 📝

This project focuses on the comparison and analysis of the RetNet vs the Transformer architecture, utilizing Microsoft's TorchScale library for implementation. More information can be found in our paper [Are You Using Retentive Networks?](./301R_Retnet_Paper.pdf).

## Reference to Original Paper

Our study is based on research detailed in the paper [Retentive Network: A Successor to Transformer for Large Language Models](https://arxiv.org/abs/2307.08621). For more in-depth information and methodology of the RetNet architecture, refer to this paper.

## Base Architecture - Microsoft TorchScale

This project is built upon [Microsoft TorchScale](https://github.com/microsoft/torchscale), which provides basic implementations of the two architectures for our research. TorchScale provides a library of foundational architecture implementations for training Transformer-based deep learning models. We have leveraged its capabilities to develop our comparison between RetNets and Transformers.

## Installation and Setup

To get started with this project, first clone this repository using the following command:

```bash
git clone https://github.com/DRAGNLabs/301r_retnet.git
cd 301r_retnet
```

### Python Version Requirement

Ensure you have Python 3.11 installed. If you do not have Python 3.11, you can download it from the official Python website or use a package manager.

### Setting Up Python Environment with Mamba

If you don't have Mamba installed, you can follow the [Mamba documentation](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) to get set up. Once Mamba is installed, create a new environment with Python 3.11:

```bash
# Optionally create a new Mamba environment with Python 3.11 and specify a name
mamba create -n <YOUR_ENV_NAME> python=3.11

# Activate the Mamba environment
mamba activate <YOUR_ENV_NAME>
```

### Running Shell Scripts

For running any .sh scripts, grant execution permissions using:

```bash
chmod +x <SOME_SCRIPT>..sh
```

Then, execute the script with:

```bash
./<SOME_SCRIPT>..sh
```

### Preparing the Environment

Before running the main scripts, make sure to install all the necessary dependencies:

```bash
pip install -r requirements.txt
```

### Preparing YAML Configuration Files

This project uses YAML configuration files to store all pipeline parameters and paths. The design choice of the YAML file is intended to eliminate repetition of commonly used parameters across code, as well as simplify future changes and refactors. We use a YAML file to allow developers to add new parameters as they see fit and make all settings visible to the user in one consolidated place.

To prepare a YAML config file, copy [template_config.yaml](./configs/template_config.yaml) into the [user_configs](./configs/user_configs/) folder. Fill out all parameters accordingly. Absolute paths are preferred for any path variables. The repository is setup to work flexibly with any desired directory structure.

### Execution Workflow

Once a YAML config file is prepared, you can pass this file into any script in the pipeline. Before you run any scripts, it is recommended to copy all of them into the [user_scripts](./scripts/user_scripts/) folder and modify the scripts to point to the right config file.

The expected order of script execution is as follows:
1. Change current directory to `./scripts/user_scripts`.
2. Run `download_data.sh` to fetch the necessary data.
3. Execute `train_tokenizer.sh` to prepare the tokenizer.
4. Use `tokenize_data.sh` for data tokenization.
5. Finally, run `retnet.sh` or `transformer.sh`, depending on your project needs.

For example, if you want to train a RetNet model:

```bash
cd ./scripts/user_scripts

./download_data.sh
./train_tokenizer.sh
./tokenize_data.sh

# Replace this with the model that you want to run
./retnet.sh
```

## Features

### Grid Search

The Grid Search feature is designed to systematically explore a range of hyperparameters and compare RetNet and Transformer models with corresponding parameters at each point. This evaluates both architectures with various combinations of learning rates, embedding dimensions, feed-forward dimensions, sequence lengths, and number of heads. The goal is to identify the configuration that results in the best model performance, measured in terms of loss and training efficiency.

**Code Overview:**

We implement the grid search process as follows:

- **Hyperparameters Tested:** Learning rates (`0.001`, `0.0005`, `0.0001`), embedding dimensions (`768`, `1024`, `1280`), feed-forward dimensions (`1024`, `2048`), heads (`4`, `8`), and sequence lengths (`256`, `512`) for a total of 72 unique combinations.
- **Evaluation Metric:** The models are compared based on their test loss, with a custom function `evaluate_models` indicating which model performed better.
- **Output:** Results are recorded in a CSV file, including each combination's average loss for both models, similarity scores, and training times.

**Key Functions:**

- `evaluate_models(model1, model2, model1_loss, model2_loss)`: Compares two models based on their test losses, returning a score that reflects their performance relative to each other.
- `grid_search(config)`: Conducts the grid search over the predefined ranges of hyperparameters, training both RetNet and Transformer models with each combination and logging the results.

**Usage:**

To run the grid search, ensure your configuration file is correctly set up, then execute the script with the path to your config file as an argument:

```bash
python3 ../../grid_search.py configs/user_configs/<YOUR_CONFIG_HERE>.yaml
```

### Hugging Face Integration

This feature introduces custom models built upon the Hugging Face Transformers library, enabling the incorporation of RetNet and Transformer architectures into a wide range of NLP tasks. Leveraging Hugging Face's `PreTrainedModel` class, we've developed `RetNetModelHF` and `TransformerModelHF` classes to seamlessly integrate with Hugging Face's ecosystem, facilitating easy model training, evaluation, and deployment.

**Code Overview:**

- **`RetNetModelHF`**: Implements the RetNet architecture as a subclass of PreTrainedModel, using Hugging Face's utilities and standards for model configuration, serialization, and compatibility with the Transformers library.
- **`TransformerModelHF`**: Implements the Transformer architecture as a subclass of PreTrainedModel, using Hugging Face's utilities and standards for model configuration, serialization, and compatibility with the Transformers library.

**Key Components:**

- **Configuration Classes**: Both models utilize specific configuration classes (`RetNetConfig` for RetNetModelHF and `DecoderConfig` for TransformerModelHF) to define model parameters, ensuring flexibility and ease of customization.
- **Embedding Layer**: Initializes text embeddings with a dedicated padding index, supporting efficient token representation and processing.
- **Decoder Stacks**: Incorporates specialized decoder architectures (`RetNetDecoder` and `Decoder`) tailored to each model's needs, facilitating the core computational logic for sequence processing.
- **Forward Method**: Defines the computation performed at every call, taking input tensors and producing predictions, showcasing the model's application to sequence-to-sequence tasks.

**Usage:**

To use these models within your Hugging Face-based projects, follow these steps:

1. **Initialization**: Instantiate the model with the desired configuration, which can be a predefined object, a path to a configuration file, or left as default for automatic configuration.

   ```python
   from <YOUR_MODULE> import RetNetModelHF, TransformerModelHF

   retnet_model = RetNetModelHF(config="path/to/retnet/config")
   transformer_model = TransformerModelHF(config="path/to/transformer/config")
   ```

2. **Forward Pass**: Call the model with input data tensors to receive output predictions.

   ```python
   input_ids = ...  # Your input tensor here
   retnet_output = retnet_model(input_ids)
   transformer_output = transformer_model(input_ids)
   ```

3. **Parameter Access**: Retrieve model hyperparameters for inspection or further processing.

   ```python
   retnet_params = retnet_model.get_params()
   transformer_params = transformer_model.get_params()
   ```

### PyTorch Lightning Integration

PyTorch Lightning is leveraged in our project to streamline the training process of the RetNet and Transformer models, enabling efficient multi-core processing, easier scalability, and cleaner code by abstracting the boilerplate training loops. PyTorch Lightning's integration facilitates advanced functionalities like distributed training, automated logging, and checkpointing.

**Key Advantages:**

- **Simplified Training Loop**: By abstracting the complexity of the training loop, PyTorch Lightning allows us to focus on the model architecture and the experiment itself, rather than boilerplate code.
- **Multi-Core and Distributed Training**: Lightning's built-in support for distributed training and multi-core processing significantly speeds up training times, allowing our models to leverage multiple GPUs seamlessly.
- **Automated Checkpointing**: The custom checkpointing system, `CustomModelCheckpoint`, automatically saves model checkpoints and Hugging Face compatible weights during training, facilitating model preservation and reproducibility.
- **Advanced Logging**: Integration with TensorBoard for detailed logging of training and validation metrics, helping in monitoring model performance and debugging.

**Usage:**

1. **Model Initialization**: Instantiate a model class with the desired configuration. The configuration should include model hyperparameters, training parameters, and dataset specifics.
2. **Trainer Setup**: Configure a `Trainer` object from PyTorch Lightning, specifying training options such as the number of GPUs, distributed backend, and callbacks like model checkpointing.
3. **Training Execution**: Use the `Trainer` to train the model by passing the model instance and the data module. The training process automatically handles device placement, distributed training, and logging.
4. **Evaluation and Testing**: After training, use the `Trainer` for evaluating the model on a validation set and testing it on a test set, leveraging the best model checkpoint saved during training.

### TorchScale Integration

Our project leverages **Microsoft TorchScale** as the foundational framework to enhance the training and evaluation process of deep learning models, particularly focusing on the comparative analysis between RetNet and Transformer architectures. TorchScale is a robust library offering a suite of tools and utilities designed to optimize deep learning workflows, enabling scalable and efficient model development.

**Core Contributions:**

- **Efficiency and Scalability**: TorchScale provides critical functionalities for handling large-scale datasets and models, significantly improving training speed and efficiency without compromising accuracy or model complexity.
- **Advanced Utilities**: The library includes a range of utilities for model evaluation, performance benchmarking, and hyperparameter tuning, facilitating a comprehensive analysis of model behaviors under various configurations.
- **Integration with RetNet and Transformers**: Through TorchScale, we compare the performance of RetNet and Transformer models across different metrics, ensuring fair and rigorous evaluation standards.
- **Enhanced Model Training**: TorchScale's support for distributed training and model optimization techniques allows us to train more complex models with larger datasets, pushing the boundaries of what's possible in our research.

**Implementation Highlights:**

Our project specifically benefits from TorchScale's:

- **Distributed Training Support**: Utilizing TorchScale's distributed training capabilities to expedite the training process across multiple GPUs, enabling more extensive experimentation and faster iteration cycles.
- **Performance Benchmarking Tools**: Leveraging built-in tools for benchmarking model performance, which has been crucial in the side-by-side comparison of RetNet and Transformer models, providing insights into their respective strengths and limitations.
- **Hyperparameter Tuning and Model Evaluation**: Employing TorchScale's utilities for hyperparameter optimization and model evaluation to fine-tune our models for optimal performance, ensuring our comparisons are based on the best possible configurations of each architecture.

**Usage in Our Project:**

TorchScale's integration into our workflow has been very helpful, being utilized across various stages of model development from initial training to final evaluation. This enables us to conduct a thorough and nuanced comparison of RetNet and Transformer models.

## Benchmarking and Results

We use EleutherAI's open-source language model evaluation harness to empirically evaluate our models across a suite of different NLP tasks. Run the evaluation suite as follows:
First, edit the 'tasks' parameter in the YAML file. Specify all tasks you would like to run, e.g.,
```
tasks:
  - "hellaswag"
  - "winogrande"
```
Alternatively, you can use `tasks: '*'` to run all benchmarks in the suite. Then navigate to the `slurm/run_eval.sh`, copy the script, and subsitute your yaml file for the placeholder. Finally, execute: 

```
mamba activate <YOUR_ENV_HERE> # Activate environment, if using one.
cd /301r_retnet/slurm/
cp run_eval.sh user_slurm/<NAME_OF_NEW_FILE>.sh  # Give your file a descriptive name, (e.g., 'retnet_40540_run_eval.sh')
bash <NAME_OF_NEW_FILE>/.sh
```
Results will be sent to a csv.

## Acknowledgments

We extend our heartfelt gratitude to the following individuals and institutions for their invaluable contributions to this project:

**Nancy Fulda**: Our esteemed instructor, whose guidance and insights have significantly shaped the direction and execution of this research.

**BYU Office of Research Computing**: For providing the computational resources and support that were instrumental in conducting our experiments and analyses.

**Authors of the Original RetNet Paper**: For their pioneering work in the field of deep learning, which inspired our research and provided a solid base for our explorations into RetNet and Transformers.

**Microsoft TorchScale Team**: For developing and maintaining the TorchScale framework, which served as the foundational architecture for our project, enabling us to push the boundaries of what's possible in deep learning research.

## Citations

Our paper is awaiting publication and our full citation will be given soon. Our current citations can be found on the citation section on our paper [Are You Using Retentive Networks?](./301R_Retnet_Paper.pdf).


