# Copyright 2019 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Inference demo for YAMNet."""
from __future__ import division, print_function

import sys
import os
import shutil
import numpy as np
import resampy
import soundfile as sf
import tensorflow as tf

from . import params as yamnet_params
from . import yamnet as yamnet_model

def load_yamnet_model():
    params = yamnet_params.Params()
    yamnet = yamnet_model.yamnet_frames_model(params)
    yamnet.load_weights(os.path.join('.', 'yamnet', 'yamnet.h5'))
    yamnet_classes = yamnet_model.class_names(os.path.join('.', 'yamnet', 'yamnet_class_map.csv'))
    return yamnet, params, yamnet_classes


def process_wave_file(file_path, yamnet, params):
    wav_data, sr = sf.read(file_path, dtype=np.int16)
    assert wav_data.dtype == np.int16, 'Bad sample type: %r' % wav_data.dtype
    waveform = wav_data / 32768.0
    waveform = waveform.astype('float32')

    if len(waveform.shape) > 1:
        waveform = np.mean(waveform, axis=1)
    if sr != params.sample_rate:
        waveform = resampy.resample(waveform, sr, params.sample_rate)

    return yamnet(waveform)

def print_top_predictions(prediction, yamnet_classes, file_name):
    top5_i = np.argsort(prediction)[::-1][:5]
    print(file_name, ':\n' +
          '\n'.join('  {:12s}: {:.3f}'.format(yamnet_classes[i], prediction[i])
                    for i in top5_i))

def is_music(prediction, yamnet_classes):
    music_index = np.where(yamnet_classes == 'Music')[0][0]
    return prediction[music_index] > 0.25

def create_directory():
    directory_path=os.path.join('.', 'wavFiles')
    
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")

def delete_directory():
    directory_path = os.path.join('.', 'wavFiles')

    if os.path.exists(directory_path):
        try:
            shutil.rmtree(directory_path)
            print(f"Directory '{directory_path}' deleted.")
        except OSError as e:
            print(f"Error deleting directory '{directory_path}': {str(e)}")
    else:
        print(f"Directory '{directory_path}' does not exist.")

def process_directory(total_segments):
    directory_path=os.path.join('.', 'wavFiles')

    yamnet, params, yamnet_classes = load_yamnet_model()

    for i in range(total_segments):
        file_name = f"segment{i}.wav"
        file_path = os.path.join(directory_path, file_name)
        
        if not os.path.isfile(file_path):
            print(f"File {file_path} not found.")
            continue
        
        # Process the file
        try:
            scores, embeddings, spectrogram = process_wave_file(file_path, yamnet, params)
            # Do something with scores, embeddings, spectrogram
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")
        
        prediction = np.mean(scores, axis=0)

        print_top_predictions(prediction, yamnet_classes, file_name)
        
        if is_music(prediction, yamnet_classes):
            delete_next_three_files(file_path)
        else: 
            os.remove(file_path)

def delete_next_three_files(file_path):
    for i in range(3):
        new_path = get_file_path(file_path, i + 2) 
        if os.path.exists(new_path):
            os.remove(new_path)
    
def get_file_path(file_path, increment):
    filename, file_extension = os.path.splitext(file_path)
    
    updated_filename = filename[:-1] + str(int(filename[-1]) + increment)
    return updated_filename + file_extension

