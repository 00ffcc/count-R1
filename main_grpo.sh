export CUDA_VISIBLE_DEVICES=1,2,3,4,5,6
# MODEL_PATH=/NAS/wujunkang/guizhiyu/LLaMA-Factory/saves/Qwen2.5-1.5B-Instruct/full/train_2025-03-12-14-56-39/weights
MODEL_PATH=Qwen/Qwen2.5-3B-Instruct
export VLLM_ATTENTION_BACKEND=XFORMERS
# 获取当前时间，转换为字符串
timestamp=$(date "+%Y-%m-%d_%H-%M-%S")
# 与experiment_name拼接
# EXPERIMENT_NAME=SFT-Qwen2.5-1.5B-$timestamp
EXPERIMENT_NAME=SFT-Qwen2.5-3B-$timestamp

python3 -m verl.trainer.main_ppo \
    algorithm.adv_estimator=grpo \
    data.train_files=data/counting_2_15_train.parquet \
    data.val_files=data/counting_2_15_valid.parquet \
    data.train_batch_size=48 \
    data.val_batch_size=60 \
    data.max_prompt_length=400 \
    data.max_response_length=2048 \
    actor_rollout_ref.model.path=$MODEL_PATH\
    actor_rollout_ref.actor.optim.lr=5e-7 \
    actor_rollout_ref.model.use_remove_padding=True \
    actor_rollout_ref.actor.ppo_mini_batch_size=6 \
    actor_rollout_ref.actor.ppo_micro_batch_size=6 \
    actor_rollout_ref.actor.use_kl_loss=True \
    actor_rollout_ref.actor.kl_loss_coef=0.001 \
    actor_rollout_ref.actor.kl_loss_type=low_var_kl \
    actor_rollout_ref.model.enable_gradient_checkpointing=True \
    actor_rollout_ref.actor.fsdp_config.param_offload=True \
    actor_rollout_ref.actor.fsdp_config.grad_offload=True \
    actor_rollout_ref.actor.fsdp_config.optimizer_offload=True \
    actor_rollout_ref.rollout.tensor_model_parallel_size=1 \
    actor_rollout_ref.rollout.name=vllm \
    actor_rollout_ref.rollout.gpu_memory_utilization=0.8 \
    actor_rollout_ref.rollout.n=16 \
    actor_rollout_ref.ref.fsdp_config.param_offload=True \
    algorithm.kl_ctrl.kl_coef=0.001 \
    trainer.critic_warmup=0 \
    trainer.logger=['wandb'] \
    +trainer.val_only=false \
    +trainer.val_before_train=false \
    trainer.project_name='GRPO_counting' \
    trainer.experiment_name=$EXPERIMENT_NAME \
    trainer.n_gpus_per_node=6 \
    trainer.nnodes=1 \
    trainer.default_local_dir=verl_checkpoints/$EXPERIMENT_NAME \
    trainer.default_hdfs_dir=null \
    trainer.save_freq=30 \
    trainer.test_freq=30 \
    trainer.total_epochs=50 $@ 2>&1 | tee grpo.log
