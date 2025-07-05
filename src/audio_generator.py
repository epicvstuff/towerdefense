"""
Audio Generator - Procedural Audio Synthesis Engine
Generates professional-quality game audio using mathematical waveform synthesis
"""

import math
import struct
import wave
import random
from typing import List, Tuple, Optional, Union


class AudioGenerator:
    """Procedural audio synthesis engine for tower defense game"""
    
    # Audio specifications
    SAMPLE_RATE = 44100
    BIT_DEPTH = 16
    MAX_AMPLITUDE = 32767
    CHANNELS = 1  # Mono by default
    
    # Waveform types
    SINE = "sine"
    SQUARE = "square"
    TRIANGLE = "triangle"
    SAWTOOTH = "sawtooth"
    NOISE = "noise"
    
    # Noise types
    WHITE_NOISE = "white"
    BROWN_NOISE = "brown"
    FILTERED_NOISE = "filtered"
    
    def __init__(self):
        """Initialize the audio generator"""
        self.sample_rate = self.SAMPLE_RATE
        self.bit_depth = self.BIT_DEPTH
        self.max_amplitude = self.MAX_AMPLITUDE
        
    def generate_waveform(self, wave_type: str, frequency: float, duration: float, 
                         amplitude: float = 0.5, phase: float = 0.0) -> List[float]:
        """
        Generate basic waveform data
        
        Args:
            wave_type: Type of waveform (sine, square, triangle, sawtooth, noise)
            frequency: Frequency in Hz
            duration: Duration in seconds
            amplitude: Amplitude (0.0 to 1.0)
            phase: Phase offset in radians
            
        Returns:
            List of audio samples
        """
        num_samples = int(self.sample_rate * duration)
        samples = []
        
        if wave_type == self.SINE:
            for i in range(num_samples):
                t = i / self.sample_rate
                sample = amplitude * math.sin(2 * math.pi * frequency * t + phase)
                samples.append(sample)
                
        elif wave_type == self.SQUARE:
            for i in range(num_samples):
                t = i / self.sample_rate
                sine_val = math.sin(2 * math.pi * frequency * t + phase)
                sample = amplitude * (1 if sine_val >= 0 else -1)
                samples.append(sample)
                
        elif wave_type == self.TRIANGLE:
            for i in range(num_samples):
                t = i / self.sample_rate
                # Triangle wave using arcsin of sine wave
                sine_val = math.sin(2 * math.pi * frequency * t + phase)
                sample = amplitude * (2 / math.pi) * math.asin(sine_val)
                samples.append(sample)
                
        elif wave_type == self.SAWTOOTH:
            for i in range(num_samples):
                t = i / self.sample_rate
                # Sawtooth wave: linear ramp from -1 to 1
                cycle_position = (frequency * t + phase / (2 * math.pi)) % 1
                sample = amplitude * (2 * cycle_position - 1)
                samples.append(sample)
                
        elif wave_type == self.NOISE:
            for i in range(num_samples):
                sample = amplitude * (random.random() * 2 - 1)
                samples.append(sample)
                
        else:
            raise ValueError(f"Unknown wave type: {wave_type}")
            
        return samples
    
    def apply_envelope(self, audio_data: List[float], attack: float, decay: float, 
                      sustain: float, release: float, sustain_level: float = 0.7) -> List[float]:
        """
        Apply ADSR envelope to audio data
        
        Args:
            audio_data: Input audio samples
            attack: Attack time in seconds
            decay: Decay time in seconds
            sustain: Sustain time in seconds
            release: Release time in seconds
            sustain_level: Sustain amplitude level (0.0 to 1.0)
            
        Returns:
            Audio data with envelope applied
        """
        if not audio_data:
            return audio_data
            
        num_samples = len(audio_data)
        envelope = [0.0] * num_samples
        
        # Convert times to sample counts
        attack_samples = int(attack * self.sample_rate)
        decay_samples = int(decay * self.sample_rate)
        sustain_samples = int(sustain * self.sample_rate)
        release_samples = int(release * self.sample_rate)
        
        # Ensure we don't exceed total samples
        total_envelope_samples = attack_samples + decay_samples + sustain_samples + release_samples
        if total_envelope_samples > num_samples:
            # Scale down proportionally
            scale = num_samples / total_envelope_samples
            attack_samples = int(attack_samples * scale)
            decay_samples = int(decay_samples * scale)
            sustain_samples = int(sustain_samples * scale)
            release_samples = num_samples - attack_samples - decay_samples - sustain_samples
        
        sample_idx = 0
        
        # Attack phase
        for i in range(attack_samples):
            envelope[sample_idx] = i / attack_samples
            sample_idx += 1
            
        # Decay phase
        for i in range(decay_samples):
            envelope[sample_idx] = 1.0 - (i / decay_samples) * (1.0 - sustain_level)
            sample_idx += 1
            
        # Sustain phase
        for i in range(sustain_samples):
            envelope[sample_idx] = sustain_level
            sample_idx += 1
            
        # Release phase
        for i in range(release_samples):
            if sample_idx < num_samples:
                envelope[sample_idx] = sustain_level * (1.0 - i / release_samples)
                sample_idx += 1
        
        # Apply envelope to audio data
        result = []
        for i in range(num_samples):
            result.append(audio_data[i] * envelope[i])
            
        return result
    
    def generate_noise(self, noise_type: str, duration: float, amplitude: float = 0.5) -> List[float]:
        """
        Generate different types of noise
        
        Args:
            noise_type: Type of noise (white, brown, filtered)
            duration: Duration in seconds
            amplitude: Amplitude (0.0 to 1.0)
            
        Returns:
            List of noise samples
        """
        num_samples = int(self.sample_rate * duration)
        samples = []
        
        if noise_type == self.WHITE_NOISE:
            for i in range(num_samples):
                sample = amplitude * (random.random() * 2 - 1)
                samples.append(sample)
                
        elif noise_type == self.BROWN_NOISE:
            # Brown noise (red noise) - integrated white noise
            last_sample = 0.0
            for i in range(num_samples):
                white_sample = (random.random() * 2 - 1) * 0.1
                last_sample += white_sample
                # Prevent drift
                if abs(last_sample) > 1.0:
                    last_sample *= 0.95
                samples.append(amplitude * last_sample)
                
        elif noise_type == self.FILTERED_NOISE:
            # Simple low-pass filtered white noise
            white_noise = [amplitude * (random.random() * 2 - 1) for _ in range(num_samples)]
            # Apply simple moving average filter
            filter_size = 5
            for i in range(num_samples):
                start = max(0, i - filter_size // 2)
                end = min(num_samples, i + filter_size // 2 + 1)
                filtered_sample = sum(white_noise[start:end]) / (end - start)
                samples.append(filtered_sample)
                
        else:
            raise ValueError(f"Unknown noise type: {noise_type}")
            
        return samples
    
    def frequency_modulation(self, carrier_freq: float, modulator_freq: float, 
                           mod_depth: float, duration: float, amplitude: float = 0.5) -> List[float]:
        """
        Generate frequency modulated audio
        
        Args:
            carrier_freq: Carrier frequency in Hz
            modulator_freq: Modulator frequency in Hz
            mod_depth: Modulation depth (frequency deviation)
            duration: Duration in seconds
            amplitude: Amplitude (0.0 to 1.0)
            
        Returns:
            List of FM audio samples
        """
        num_samples = int(self.sample_rate * duration)
        samples = []
        
        for i in range(num_samples):
            t = i / self.sample_rate
            # Frequency modulation: f(t) = carrier_freq + mod_depth * sin(2π * modulator_freq * t)
            instantaneous_freq = carrier_freq + mod_depth * math.sin(2 * math.pi * modulator_freq * t)
            # Integrate to get phase
            phase = 2 * math.pi * instantaneous_freq * t
            sample = amplitude * math.sin(phase)
            samples.append(sample)
            
        return samples
    
    def add_noise(self, audio_data: List[float], noise_level: float, 
                  noise_type: str = WHITE_NOISE) -> List[float]:
        """
        Add noise to existing audio data
        
        Args:
            audio_data: Input audio samples
            noise_level: Noise amplitude (0.0 to 1.0)
            noise_type: Type of noise to add
            
        Returns:
            Audio data with noise added
        """
        if not audio_data:
            return audio_data
            
        duration = len(audio_data) / self.sample_rate
        noise_samples = self.generate_noise(noise_type, duration, noise_level)
        
        result = []
        for i in range(len(audio_data)):
            result.append(audio_data[i] + noise_samples[i])
            
        return result
    
    def mix_audio(self, *audio_streams: List[float], weights: Optional[List[float]] = None) -> List[float]:
        """
        Mix multiple audio streams together
        
        Args:
            audio_streams: Multiple audio sample lists
            weights: Optional weights for each stream
            
        Returns:
            Mixed audio samples
        """
        if not audio_streams:
            return []
            
        # Find the maximum length
        max_length = max(len(stream) for stream in audio_streams)
        
        # Set default weights if not provided
        if weights is None:
            weights = [1.0] * len(audio_streams)
        elif len(weights) != len(audio_streams):
            raise ValueError("Number of weights must match number of audio streams")
        
        result = [0.0] * max_length
        
        for i, stream in enumerate(audio_streams):
            weight = weights[i]
            for j in range(len(stream)):
                result[j] += stream[j] * weight
                
        return result
    
    def normalize_audio(self, audio_data: List[float], target_amplitude: float = 0.9) -> List[float]:
        """
        Normalize audio to prevent clipping
        
        Args:
            audio_data: Input audio samples
            target_amplitude: Target maximum amplitude (0.0 to 1.0)
            
        Returns:
            Normalized audio samples
        """
        if not audio_data:
            return audio_data
            
        max_amplitude = max(abs(sample) for sample in audio_data)
        if max_amplitude == 0:
            return audio_data
            
        scale_factor = target_amplitude / max_amplitude
        return [sample * scale_factor for sample in audio_data]
    
    def apply_fade(self, audio_data: List[float], fade_in: float = 0.0, 
                   fade_out: float = 0.0) -> List[float]:
        """
        Apply fade in/out to audio data
        
        Args:
            audio_data: Input audio samples
            fade_in: Fade in time in seconds
            fade_out: Fade out time in seconds
            
        Returns:
            Audio data with fades applied
        """
        if not audio_data:
            return audio_data
            
        num_samples = len(audio_data)
        fade_in_samples = int(fade_in * self.sample_rate)
        fade_out_samples = int(fade_out * self.sample_rate)
        
        result = audio_data.copy()
        
        # Apply fade in
        for i in range(min(fade_in_samples, num_samples)):
            fade_factor = i / fade_in_samples
            result[i] *= fade_factor
            
        # Apply fade out
        for i in range(min(fade_out_samples, num_samples)):
            fade_factor = (fade_out_samples - i) / fade_out_samples
            result[num_samples - 1 - i] *= fade_factor
            
        return result
    
    def save_wav_file(self, audio_data: List[float], filename: str, 
                     normalize: bool = True) -> None:
        """
        Save audio data to WAV file
        
        Args:
            audio_data: Audio samples to save
            filename: Output filename
            normalize: Whether to normalize the audio
        """
        if not audio_data:
            print(f"Warning: No audio data to save for {filename}")
            return
            
        # Normalize if requested
        if normalize:
            audio_data = self.normalize_audio(audio_data, 0.9)
        
        # Convert to 16-bit integers
        audio_data_int = []
        for sample in audio_data:
            # Clamp to valid range
            sample = max(-1.0, min(1.0, sample))
            int_sample = int(sample * self.max_amplitude)
            audio_data_int.append(int_sample)
        
        # Create WAV file
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(self.CHANNELS)
            wav_file.setsampwidth(self.bit_depth // 8)
            wav_file.setframerate(self.sample_rate)
            
            # Pack audio data
            packed_data = struct.pack(f'<{len(audio_data_int)}h', *audio_data_int)
            wav_file.writeframes(packed_data)
            
        print(f"Generated audio file: {filename}")
    
    def generate_complex_tone(self, fundamental_freq: float, harmonics: List[Tuple[float, float]], 
                            duration: float, amplitude: float = 0.5) -> List[float]:
        """
        Generate complex tone with harmonics
        
        Args:
            fundamental_freq: Fundamental frequency in Hz
            harmonics: List of (harmonic_ratio, amplitude) tuples
            duration: Duration in seconds
            amplitude: Overall amplitude (0.0 to 1.0)
            
        Returns:
            Complex tone audio samples
        """
        audio_streams = []
        weights = []
        
        # Add fundamental frequency
        fundamental = self.generate_waveform(self.SINE, fundamental_freq, duration, amplitude)
        audio_streams.append(fundamental)
        weights.append(1.0)
        
        # Add harmonics
        for harmonic_ratio, harmonic_amp in harmonics:
            harmonic_freq = fundamental_freq * harmonic_ratio
            harmonic_wave = self.generate_waveform(self.SINE, harmonic_freq, duration, 
                                                 amplitude * harmonic_amp)
            audio_streams.append(harmonic_wave)
            weights.append(harmonic_amp)
        
        return self.mix_audio(*audio_streams, weights=weights)
    
    def generate_sweep(self, start_freq: float, end_freq: float, duration: float, 
                      wave_type: str = SINE, amplitude: float = 0.5) -> List[float]:
        """
        Generate frequency sweep
        
        Args:
            start_freq: Starting frequency in Hz
            end_freq: Ending frequency in Hz
            duration: Duration in seconds
            wave_type: Type of waveform
            amplitude: Amplitude (0.0 to 1.0)
            
        Returns:
            Frequency sweep audio samples
        """
        num_samples = int(self.sample_rate * duration)
        samples = []
        
        for i in range(num_samples):
            t = i / self.sample_rate
            # Linear frequency interpolation
            freq = start_freq + (end_freq - start_freq) * (t / duration)
            
            if wave_type == self.SINE:
                # For sweeps, we need to integrate frequency to get phase
                phase = 2 * math.pi * (start_freq * t + 0.5 * (end_freq - start_freq) * t * t / duration)
                sample = amplitude * math.sin(phase)
            else:
                # For other waveforms, use instantaneous frequency
                sample = amplitude * math.sin(2 * math.pi * freq * t)
                
            samples.append(sample)
            
        return samples


# Test functions for verification
def test_basic_waveforms():
    """Test basic waveform generation"""
    print("Testing basic waveforms...")
    generator = AudioGenerator()
    
    # Test each waveform type
    waveforms = [
        (AudioGenerator.SINE, "sine_test.wav"),
        (AudioGenerator.SQUARE, "square_test.wav"),
        (AudioGenerator.TRIANGLE, "triangle_test.wav"),
        (AudioGenerator.SAWTOOTH, "sawtooth_test.wav"),
        (AudioGenerator.NOISE, "noise_test.wav")
    ]
    
    for wave_type, filename in waveforms:
        audio = generator.generate_waveform(wave_type, 440.0, 1.0, 0.5)
        generator.save_wav_file(audio, f"test_{filename}")
    
    print("Basic waveform tests completed!")


def test_envelope():
    """Test ADSR envelope"""
    print("Testing ADSR envelope...")
    generator = AudioGenerator()
    
    # Generate sine wave
    audio = generator.generate_waveform(AudioGenerator.SINE, 440.0, 2.0, 0.8)
    
    # Apply envelope
    enveloped = generator.apply_envelope(audio, 0.1, 0.3, 1.0, 0.6, 0.7)
    
    generator.save_wav_file(enveloped, "test_envelope.wav")
    print("Envelope test completed!")


def test_noise_generation():
    """Test noise generation"""
    print("Testing noise generation...")
    generator = AudioGenerator()
    
    noise_types = [
        (AudioGenerator.WHITE_NOISE, "white_noise_test.wav"),
        (AudioGenerator.BROWN_NOISE, "brown_noise_test.wav"),
        (AudioGenerator.FILTERED_NOISE, "filtered_noise_test.wav")
    ]
    
    for noise_type, filename in noise_types:
        noise = generator.generate_noise(noise_type, 1.0, 0.5)
        generator.save_wav_file(noise, f"test_{filename}")
    
    print("Noise generation tests completed!")


def test_frequency_modulation():
    """Test frequency modulation"""
    print("Testing frequency modulation...")
    generator = AudioGenerator()
    
    fm_audio = generator.frequency_modulation(440.0, 5.0, 50.0, 2.0, 0.5)
    generator.save_wav_file(fm_audio, "test_fm.wav")
    
    print("Frequency modulation test completed!")


def test_complex_features():
    """Test complex audio features"""
    print("Testing complex features...")
    generator = AudioGenerator()
    
    # Test complex tone with harmonics
    harmonics = [(2.0, 0.5), (3.0, 0.3), (4.0, 0.2)]
    complex_tone = generator.generate_complex_tone(220.0, harmonics, 2.0, 0.6)
    generator.save_wav_file(complex_tone, "test_complex_tone.wav")
    
    # Test frequency sweep
    sweep = generator.generate_sweep(200.0, 800.0, 2.0, AudioGenerator.SINE, 0.5)
    generator.save_wav_file(sweep, "test_sweep.wav")
    
    print("Complex features tests completed!")


if __name__ == "__main__":
    print("AudioGenerator Test Suite")
    print("=" * 40)
    
    test_basic_waveforms()
    test_envelope()
    test_noise_generation()
    test_frequency_modulation()
    test_complex_features()
    
    print("\nAll tests completed! Check generated test files.") 