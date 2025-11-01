'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Upload, Loader, Play, Pause, RotateCcw, AlertCircle, FileAudio } from 'lucide-react';

// Get API URL from environment or default to localhost:8000
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface VoiceRecorderProps {
  onTranscriptionComplete: (text: string, language: string) => void;
  isLoading?: boolean;
}

export function VoiceRecorder({
  onTranscriptionComplete,
  isLoading = false,
}: VoiceRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [language, setLanguage] = useState<string>('en');
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackTime, setPlaybackTime] = useState(0);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [uploadMode, setUploadMode] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [uploadedAudioUrl, setUploadedAudioUrl] = useState<string | null>(null);
  const [uploadedDuration, setUploadedDuration] = useState(0);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const timerIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const audioPlayerRef = useRef<HTMLAudioElement | null>(null);
  const playbackIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const uploadPlayerRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    return () => {
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
      }
      if (playbackIntervalRef.current) {
        clearInterval(playbackIntervalRef.current);
      }
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);

      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        // Stop all tracks
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();

      setIsRecording(true);
      setRecordingTime(0);

      // Timer
      timerIntervalRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert(
        'Unable to access microphone. Please check permissions and try again.'
      );
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setError(null);

      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
      }

      // Create audio URL for playback
      setTimeout(() => {
        if (audioChunksRef.current.length > 0) {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
          const url = URL.createObjectURL(audioBlob);
          setAudioUrl(url);
        }
      }, 100);
    }
  };

  const playAudio = () => {
    if (audioPlayerRef.current) {
      audioPlayerRef.current.play();
      setIsPlaying(true);
    }
  };

  const pauseAudio = () => {
    if (audioPlayerRef.current) {
      audioPlayerRef.current.pause();
      setIsPlaying(false);
    }
  };

  const resetRecording = () => {
    audioChunksRef.current = [];
    setAudioUrl(null);
    setRecordingTime(0);
    setPlaybackTime(0);
    setIsPlaying(false);
    setError(null);
    if (audioPlayerRef.current) {
      audioPlayerRef.current.currentTime = 0;
    }
  };

  const submitAudio = async () => {
    if (audioChunksRef.current.length === 0) {
      alert('No audio recorded');
      return;
    }

    setIsTranscribing(true);

    try {
      const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });

      if (audioBlob.size === 0) {
        setError('Audio file is empty. Please record again.');
        return;
      }

      console.log('Sending audio to API:', {
        size: audioBlob.size,
        type: audioBlob.type,
        language: language,
      });

      // Create FormData for file upload
      const formData = new FormData();
      formData.append('file', audioBlob, 'audio.webm');
      formData.append('language', language);

      // Call transcription API with full URL
      const response = await fetch(`${API_URL}/api/transcription/transcribe`, {
        method: 'POST',
        body: formData,
      });

      console.log('API response status:', response.status);

      if (!response.ok) {
        const errorData = await response.json();
        console.error('API error:', errorData);
        throw new Error(errorData.detail || `Transcription failed (${response.status})`);
      }

      const result = await response.json();
      console.log('Transcription result:', result);

      if (!result.text) {
        setError('No text was transcribed. Please try again with clearer audio.');
        return;
      }

      // Call parent callback with transcribed text and detected language
      onTranscriptionComplete(result.text, result.language);

      // Reset recorder
      resetRecording();
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      console.error('Transcription error:', errorMessage);
      setError(`Transcription failed: ${errorMessage}`);
    } finally {
      setIsTranscribing(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs
      .toString()
      .padStart(2, '0')}`;
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file type
    const validTypes = ['audio/mpeg', 'audio/wav', 'audio/webm', 'audio/ogg', 'audio/m4a', 'audio/aac'];
    if (!validTypes.includes(file.type) && !file.name.match(/\.(mp3|wav|webm|ogg|m4a|aac)$/i)) {
      setError('Please select a valid audio file (MP3, WAV, WebM, OGG, M4A, or AAC)');
      return;
    }

    // Validate file size (max 100MB)
    const maxSize = 100 * 1024 * 1024;
    if (file.size > maxSize) {
      setError('Audio file is too large. Maximum size is 100MB.');
      return;
    }

    setError(null);
    setUploadedFile(file);
    setUploadMode(true);

    // Create preview URL
    const url = URL.createObjectURL(file);
    setUploadedAudioUrl(url);
  };

  const handleAudioLoadedMetadata = (e: React.SyntheticEvent<HTMLAudioElement>) => {
    const audio = e.currentTarget;
    setUploadedDuration(Math.floor(audio.duration));
  };

  const resetUpload = () => {
    setUploadedFile(null);
    setUploadedAudioUrl(null);
    setUploadedDuration(0);
    setUploadMode(false);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    if (uploadPlayerRef.current) {
      uploadPlayerRef.current.currentTime = 0;
    }
  };

  const submitUploadedAudio = async () => {
    if (!uploadedFile) {
      setError('No file selected');
      return;
    }

    setIsTranscribing(true);
    setError(null);

    try {
      console.log('Uploading audio file:', {
        name: uploadedFile.name,
        size: uploadedFile.size,
        type: uploadedFile.type,
        language: language,
      });

      const formData = new FormData();
      formData.append('file', uploadedFile);
      formData.append('language', language);

      const response = await fetch(`${API_URL}/api/transcription/transcribe`, {
        method: 'POST',
        body: formData,
      });

      console.log('Upload API response status:', response.status);

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Upload API error:', errorData);
        throw new Error(errorData.detail || `Upload failed (${response.status})`);
      }

      const result = await response.json();
      console.log('Upload transcription result:', result);

      if (!result.text) {
        setError('No text was transcribed. Please try a different audio file.');
        return;
      }

      // Call parent callback with transcribed text and detected language
      onTranscriptionComplete(result.text, result.language);

      // Reset uploader
      resetUpload();
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      console.error('Upload transcription error:', errorMessage);
      setError(`Upload failed: ${errorMessage}`);
    } finally {
      setIsTranscribing(false);
    }
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
      {/* Error Message */}
      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
          <AlertCircle size={18} className="text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-red-900">{error}</p>
            <p className="text-xs text-red-700 mt-1">Check browser console (F12) for details</p>
          </div>
        </div>
      )}

      {/* Mode Selector Tabs */}
      {!uploadMode && !audioUrl && (
        <div className="flex gap-2 mb-4 border-b border-gray-200">
          <button
            className="px-4 py-2 text-sm font-medium text-gray-700 border-b-2 border-transparent hover:text-gray-900 transition-colors"
            style={{ borderColor: !uploadMode ? '#3b82f6' : 'transparent' }}
            onClick={() => setUploadMode(false)}
            disabled={isRecording}
          >
            🎤 Record Audio
          </button>
          <button
            className="px-4 py-2 text-sm font-medium text-gray-700 border-b-2 border-transparent hover:text-gray-900 transition-colors"
            style={{ borderColor: uploadMode ? '#3b82f6' : 'transparent' }}
            onClick={() => setUploadMode(true)}
            disabled={isRecording}
          >
            📁 Upload Audio
          </button>
        </div>
      )}

      {/* Recording Controls */}
      {!uploadMode && (
      <div className="flex items-center gap-4 mb-4">
        {/* Microphone Button */}
        <div className="flex-shrink-0">
          {!isRecording ? (
            <button
              onClick={startRecording}
              disabled={isLoading || isTranscribing || audioUrl !== null}
              className="p-3 rounded-full bg-red-100 hover:bg-red-200 text-red-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              title="Start recording"
            >
              <Mic size={24} />
            </button>
          ) : (
            <button
              onClick={stopRecording}
              className="p-3 rounded-full bg-red-500 hover:bg-red-600 text-white animate-pulse transition-colors"
              title="Stop recording"
            >
              <Square size={24} />
            </button>
          )}
        </div>

        {/* Recording Info */}
        <div className="flex-1">
          {isRecording ? (
            <div className="flex items-center gap-3">
              <div className="text-sm font-semibold text-red-600">
                Recording... {formatTime(recordingTime)}
              </div>
              <div className="flex gap-1">
                <div className="w-1 h-4 bg-red-600 rounded-full animate-bounce" />
                <div className="w-1 h-4 bg-red-600 rounded-full animate-bounce animation-delay-200" />
                <div className="w-1 h-4 bg-red-600 rounded-full animate-bounce animation-delay-400" />
              </div>
            </div>
          ) : audioUrl ? (
            <div className="text-sm text-gray-600">
              Recording ready • {formatTime(recordingTime)} seconds
            </div>
          ) : (
            <div className="text-sm text-gray-500">
              Click the microphone icon to start recording
            </div>
          )}
        </div>

      </div>
      )}

      {/* Upload Controls */}
      {uploadMode && (
        <div className="space-y-4">
          {/* File Input (Hidden) */}
          <input
            ref={fileInputRef}
            type="file"
            accept="audio/*"
            onChange={handleFileSelect}
            className="hidden"
            disabled={isTranscribing}
          />

          {/* Upload Button or File Info */}
          {!uploadedFile ? (
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={isTranscribing}
              className="w-full py-3 px-4 bg-blue-50 border-2 border-dashed border-blue-300 rounded-lg hover:bg-blue-100 text-blue-700 font-medium flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <FileAudio size={20} />
              Click to upload audio file or drag and drop
            </button>
          ) : (
            <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-center gap-3">
                <FileAudio size={20} className="text-blue-600 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-blue-900 truncate">{uploadedFile.name}</p>
                  <p className="text-xs text-blue-700">
                    {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB • {formatTime(uploadedDuration)}
                  </p>
                </div>
                <button
                  onClick={resetUpload}
                  disabled={isTranscribing}
                  className="p-2 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-600 disabled:opacity-50 transition-colors flex-shrink-0"
                  title="Remove file"
                >
                  <RotateCcw size={16} />
                </button>
              </div>

              {/* Audio Player for Upload */}
              {uploadedAudioUrl && (
                <div className="mt-3">
                  <audio
                    ref={uploadPlayerRef}
                    src={uploadedAudioUrl}
                    className="w-full"
                    controls
                    onLoadedMetadata={handleAudioLoadedMetadata}
                  />
                </div>
              )}

              {/* Submit Button */}
              <button
                onClick={submitUploadedAudio}
                disabled={isTranscribing}
                className="w-full mt-3 py-2 px-4 bg-green-100 hover:bg-green-200 text-green-700 font-medium rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isTranscribing ? (
                  <>
                    <Loader size={16} className="animate-spin" />
                    Transcribing...
                  </>
                ) : (
                  <>
                    <Upload size={16} />
                    Transcribe Audio
                  </>
                )}
              </button>

              {isTranscribing && (
                <div className="mt-2 text-sm text-blue-700 flex items-center gap-2">
                  <Loader size={14} className="animate-spin" />
                  Transcribing audio... This may take 5-10 seconds
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Playback Controls */}
      {audioUrl && !isRecording && (
        <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-center gap-3">
            <button
              onClick={isPlaying ? pauseAudio : playAudio}
              disabled={isTranscribing}
              className="p-2 rounded-full bg-blue-100 hover:bg-blue-200 text-blue-600 disabled:opacity-50 transition-colors flex-shrink-0"
              title={isPlaying ? 'Pause' : 'Play'}
            >
              {isPlaying ? <Pause size={18} /> : <Play size={18} />}
            </button>

            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <audio
                  ref={audioPlayerRef}
                  src={audioUrl}
                  className="flex-1"
                  onEnded={() => setIsPlaying(false)}
                  onTimeUpdate={(e) => {
                    setPlaybackTime(Math.floor(e.currentTarget.currentTime));
                  }}
                />
              </div>
              <div className="text-xs text-gray-600 mt-1">
                {formatTime(playbackTime)} / {formatTime(recordingTime)}
              </div>
            </div>

            <button
              onClick={resetRecording}
              disabled={isTranscribing}
              className="p-2 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-600 disabled:opacity-50 transition-colors flex-shrink-0"
              title="Reset recording"
            >
              <RotateCcw size={18} />
            </button>

            <button
              onClick={submitAudio}
              disabled={isTranscribing || isLoading}
              className="p-2 rounded-full bg-green-100 hover:bg-green-200 text-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex-shrink-0"
              title="Transcribe audio"
            >
              {isTranscribing ? (
                <Loader size={18} className="animate-spin" />
              ) : (
                <Upload size={18} />
              )}
            </button>
          </div>

          {isTranscribing && (
            <div className="mt-3 text-sm text-blue-700 flex items-center gap-2">
              <Loader size={14} className="animate-spin" />
              Transcribing audio... This may take 5-10 seconds
            </div>
          )}
        </div>
      )}
    </div>
  );
}
