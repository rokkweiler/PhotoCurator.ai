Technical
{
  "train_env": "TID2013",
  "docker_image": "nima-cpu",
  "base_model_name": "MobileNet",
  "existing_weights": null,
  "n_classes": 10,
  "batch_size": 8,
  "epochs_train_dense": 1,
  "learning_rate_dense": 0.001,
  "decay_dense": 0,
  "epochs_train_all": 5,
  "learning_rate_all": 0.0000003,
  "decay_all": 0,
  "dropout_rate": 0.75,
  "multiprocessing_data_load": false,
  "num_workers_data_load": 10,
  "img_format": "bmp"
}

Aesthetic
{                                            {
  "train_env": "remote",
  "docker_image": "nima-cpu",
  "base_model_name": "MobileNet",
  "existing_weights": null,
  "n_classes": 10,
  "batch_size": 96,
  "epochs_train_dense": 5,
  "learning_rate_dense": 0.001,
  "decay_dense": 0,
  "epochs_train_all": 9,
  "learning_rate_all": 0.00003,
  "decay_all": 0.000023,
  "l2_reg": null,
  "dropout_rate": 0.75,
  "multiprocessing_data_load": false,
  "num_workers_data_load": 1
}

BIRDS AESTHETIC
{
  "train_env": "remote",
  "docker_image": "nima-cpu",
  "base_model_name": "MobileNet",
  "existing_weights": null,
  "n_classes": 10,
  "batch_size": 8,
  "epochs_train_dense": 10,
  "learning_rate_dense": 0.0001,
  "decay_dense": 0,
  "epochs_train_all": 15,
  "learning_rate_all": 0.00001,
  "decay_all": 0.00001,
  "l2_reg": 0.0001,
  "dropout_rate": 0.5,
  "multiprocessing_data_load": false,
  "num_workers_data_load": 1
}

BIRDS Technical
{                                       {
  "train_env": "TID2013",
  "docker_image": "nima-cpu",
  "base_model_name": "MobileNet",
  "existing_weights": null,
  "n_classes": 10,
  "batch_size": 8,
  "epochs_train_dense": 10,
  "learning_rate_dense": 0.0001,
  "decay_dense": 0,
  "epochs_train_all": 15,
  "learning_rate_all": 0.00001,
  "decay_all": 0.00001,
  "dropout_rate": 0.5,
  "multiprocessing_data_load": false,
  "num_workers_data_load": 1,
  "img_format": "jpg"
}

#aesthetic train script
bash ./train-local \
--config-file $(pwd)/models/MobileNet/config_aesthetic_cpu_custom_birds.json \
--samples-file /mnt/c/Users/ryanr/OneDrive/Pictures/trainingimages/bird_training.json \
--image-dir /mnt/c/Users/ryanr/OneDrive/Pictures/trainingimages

#aesthetic save file
/train_jobs/2024_08_14_14_37_00/weights/weights_mobilenet_23_0.310.hdf5

#aesthetic test models
bash ./predict \
--docker-image nima-cpu \
--base-model-name MobileNet \
--weights-file $(pwd)/train_jobs/2024_08_14_14_37_00/weights/weights_mobilenet_23_0.310.hdf5 \
--image-source /mnt/c/Users/ryanr/OneDrive/Pictures/testimages



#technical train script
bash ./train-local \
--config-file $(pwd)/models/MobileNet/config_technical_cpu_custom_birds.json \
--samples-file /mnt/c/Users/ryanr/OneDrive/Pictures/trainingimages/bird_training.json \
--image-dir /mnt/c/Users/ryanr/OneDrive/Pictures/trainingimages

#technical save file
/train_jobs/2024_08_14_15_26_57/weights/weights_mobilenet_25_0.246.hdf5

#technical test models
bash ./predict \
--docker-image nima-cpu \
--base-model-name MobileNet \
--weights-file $(pwd)/train_jobs/2024_08_14_15_26_57/weights/weights_mobilenet_25_0.246.hdf5 \
--image-source /mnt/c/Users/ryanr/OneDrive/Pictures/testimages



#log....
stream the logs
CONTAINER_ID=$(docker ps -l -q)
docker logs $CONTAINER_ID --follow

#stop....
stop
CONTAINER_ID=$(docker ps -l -q)
docker container stop $CONTAINER_ID