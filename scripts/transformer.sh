python3 ../train_model.py \
    --activation-dropout 0.1 \
    --batch-size 128 \
    --checkpoints \
    --dataset-feature text \
    --dataset-name c4 \
    --dataset-subset en \
    --device cuda \
    --dropout 0.1 \
    --embed-dim 128 \
    --epochs 10 \
    --ffn-dim 1024 \
    --fsdp \
    --layers 6 \
    --lr 0.001 \
    --model transformer \
    --heads 8 \
    --rand-seed 42 \
    --seq-len 128 \
    --splits 0.7 0.2 0.1 \
    --val-freq 3 \
    --value-embed-dim 128 \
    --vocab-size 100000 \
