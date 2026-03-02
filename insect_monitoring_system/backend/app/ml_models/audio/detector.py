import numpy as np
import librosa
# import tflite_runtime.interpreter as tflite # Use this on device
import tensorflow as tf # Use this for local development

# Placeholder for TFLite model
# interpreter = tflite.Interpreter(model_path="insect_sound_model.tflite")
# interpreter.allocate_tensors()

def preprocess_audio(audio_file, sample_rate=22050, n_mfcc=13, max_len=174):
    """
    Extracts MFCCs from an audio file.
    """
    try:
        audio, sr = librosa.load(audio_file, sr=sample_rate)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
        
        # Pad or truncate
        if mfccs.shape[1] > max_len:
            mfccs = mfccs[:, :max_len]
        else:
            pad_width = max_len - mfccs.shape[1]
            mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
            
        return mfccs
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return None

def classify_insect_sound(audio_file):
    """
    Classifies insect sound from an audio file using a TFLite model.
    """
    mfccs = preprocess_audio(audio_file)
    if mfccs is None:
        return {"error": "Failed to process audio"}

    # Reshape for model input
    mfccs = mfccs[np.newaxis, ..., np.newaxis]

    # # TFLite inference
    # input_details = interpreter.get_input_details()
    # output_details = interpreter.get_output_details()
    # interpreter.set_tensor(input_details[0]['index'], mfccs.astype(np.float32))
    # interpreter.invoke()
    # output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Placeholder for classification result
    # predicted_class_index = np.argmax(output_data)
    # class_names = ['Cricket', 'Cicada', 'Other'] # Example
    # predicted_class = class_names[predicted_class_index]

    return {"predicted_class": "Cicada"} # Placeholder