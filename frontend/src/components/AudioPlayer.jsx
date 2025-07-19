// src/components/AudioPlayer.jsx - Player audio per le voci di Aether

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { aetherAPI, getAudioURL } from '../services/api';
import { 
  Play, 
  Pause, 
  SkipBack, 
  SkipForward, 
  Volume2, 
  VolumeX,
  Music,
  Download,
  Clock
} from 'lucide-react';

const AudioTrack = ({ track, isPlaying, onPlay, onDownload }) => {
  const formatDuration = (duration) => {
    if (!duration) return '--:--';
    const minutes = Math.floor(duration / 60);
    const seconds = Math.floor(duration % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const formatFileSize = (size) => {
    if (!size) return 'N/A';
    return `${(size / 1024).toFixed(1)}KB`;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`
        bg-gray-900 bg-opacity-50 backdrop-blur-sm border border-gray-700 
        rounded-lg p-3 transition-all duration-300 group
        ${isPlaying ? 'ring-2 ring-cyan-400 border-cyan-400' : 'hover:border-gray-500'}
      `}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3 flex-1 min-w-0">
          {/* Play button */}
          <button
            onClick={() => onPlay(track)}
            className={`
              w-8 h-8 rounded-full flex items-center justify-center transition-colors
              ${isPlaying 
                ? 'bg-cyan-500 text-white' 
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }
            `}
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 ml-0.5" />}
          </button>

          {/* Track info */}
          <div className="flex-1 min-w-0">
            <h4 className="text-white text-sm font-medium truncate">
              {track.name || 'Audio Aether'}
            </h4>
            <div className="flex items-center gap-3 text-xs text-gray-500">
              <span>{formatDuration(track.duration)}</span>
              <span>{formatFileSize(track.size)}</span>
              <span>{new Date(track.created).toLocaleDateString()}</span>
            </div>
          </div>
        </div>

        {/* Download button */}
        <button
          onClick={() => onDownload(track)}
          className="w-8 h-8 rounded-full bg-gray-700 hover:bg-gray-600 text-gray-300 flex items-center justify-center transition-colors opacity-0 group-hover:opacity-100"
        >
          <Download className="w-4 h-4" />
        </button>
      </div>

      {/* Playing indicator */}
      {isPlaying && (
        <div className="mt-2 flex items-center gap-1">
          <div className="flex items-center gap-0.5">
            {[...Array(5)].map((_, i) => (
              <div
                key={i}
                className="w-1 bg-cyan-400 rounded-full animate-pulse"
                style={{
                  height: `${Math.random() * 12 + 4}px`,
                  animationDelay: `${i * 0.1}s`
                }}
              />
            ))}
          </div>
          <span className="text-xs text-cyan-400 ml-2">In riproduzione...</span>
        </div>
      )}
    </motion.div>
  );
};

const AudioPlayer = () => {
  const [audioFiles, setAudioFiles] = useState([]);
  const [currentTrack, setCurrentTrack] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const audioRef = useRef(null);

  const fetchAudioFiles = async () => {
    try {
      setLoading(true);
      const data = await aetherAPI.getAudioFiles();
      
      if (data.error) {
        setError(data.error);
        return;
      }

      setAudioFiles(data.audio_files || []);
      setError(null);
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const playTrack = (track) => {
    try {
      if (currentTrack?.filename === track.filename && isPlaying) {
        // Pause current track
        audioRef.current?.pause();
        setIsPlaying(false);
        return;
      }

      // Load new track
      if (audioRef.current) {
        audioRef.current.src = getAudioURL(track.filename);
        audioRef.current.load();
        
        audioRef.current.play().then(() => {
          setCurrentTrack(track);
          setIsPlaying(true);
        }).catch(err => {
          console.error('Error playing audio:', err);
        });
      }
    } catch (error) {
      console.error('Error in playTrack:', error);
    }
  };

  const downloadTrack = (track) => {
    try {
      const link = document.createElement('a');
      link.href = getAudioURL(track.filename);
      link.download = track.filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading track:', error);
    }
  };

  const handleVolumeChange = (newVolume) => {
    setVolume(newVolume);
    if (audioRef.current) {
      audioRef.current.volume = newVolume;
    }
  };

  const toggleMute = () => {
    setIsMuted(!isMuted);
    if (audioRef.current) {
      audioRef.current.muted = !isMuted;
    }
  };

  const formatTime = (time) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  useEffect(() => {
    fetchAudioFiles();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchAudioFiles, 30000);
    
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleTimeUpdate = () => setCurrentTime(audio.currentTime);
    const handleDurationChange = () => setDuration(audio.duration);
    const handleEnded = () => {
      setIsPlaying(false);
      setCurrentTime(0);
    };

    audio.addEventListener('timeupdate', handleTimeUpdate);
    audio.addEventListener('durationchange', handleDurationChange);
    audio.addEventListener('ended', handleEnded);

    return () => {
      audio.removeEventListener('timeupdate', handleTimeUpdate);
      audio.removeEventListener('durationchange', handleDurationChange);
      audio.removeEventListener('ended', handleEnded);
    };
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <Music className="w-8 h-8 animate-pulse text-cyan-400 mx-auto mb-2" />
          <p className="text-gray-400">Caricamento file audio...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900 bg-opacity-20 border border-red-500 rounded-lg p-4 text-red-400">
        <h3 className="font-bold mb-2">⚠️ Errore Caricamento Audio</h3>
        <p className="text-sm">{error}</p>
        <button
          onClick={fetchAudioFiles}
          className="mt-3 px-4 py-2 bg-red-600 hover:bg-red-700 rounded text-white text-sm transition-colors"
        >
          Riprova
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Music className="w-6 h-6" />
          Audio Aether ({audioFiles.length})
        </h2>
        <button
          onClick={fetchAudioFiles}
          className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm text-white transition-colors"
        >
          Aggiorna
        </button>
      </div>

      {/* Current track controls */}
      {currentTrack && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gray-800 rounded-lg p-4 space-y-3"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-cyan-500 to-purple-500 rounded-full flex items-center justify-center">
                🎵
              </div>
              <div>
                <h3 className="text-white font-medium">{currentTrack.name || 'Audio Aether'}</h3>
                <p className="text-gray-400 text-sm">Voce di Aether</p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              {/* Volume control */}
              <button onClick={toggleMute} className="text-gray-400 hover:text-white">
                {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
              </button>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={isMuted ? 0 : volume}
                onChange={(e) => handleVolumeChange(parseFloat(e.target.value))}
                className="w-20"
              />
            </div>
          </div>

          {/* Progress bar */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs text-gray-400">
              <span>{formatTime(currentTime)}</span>
              <span>{formatTime(duration)}</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div
                className="bg-cyan-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${duration ? (currentTime / duration) * 100 : 0}%` }}
              />
            </div>
          </div>
        </motion.div>
      )}

      {/* Audio files list */}
      {audioFiles.length === 0 ? (
        <div className="text-center py-12">
          <Music className="w-12 h-12 text-gray-600 mx-auto mb-4" />
          <h3 className="text-gray-400 text-lg mb-2">Nessun File Audio</h3>
          <p className="text-gray-500 text-sm">
            Aether non ha ancora generato file audio. Attendere la sintesi vocale...
          </p>
        </div>
      ) : (
        <div className="space-y-2 max-h-96 overflow-y-auto">
          <AnimatePresence>
            {audioFiles.map((track, index) => (
              <AudioTrack
                key={track.filename || index}
                track={track}
                isPlaying={currentTrack?.filename === track.filename && isPlaying}
                onPlay={playTrack}
                onDownload={downloadTrack}
              />
            ))}
          </AnimatePresence>
        </div>
      )}

      {/* Hidden audio element */}
      <audio
        ref={audioRef}
        volume={volume}
        muted={isMuted}
        preload="metadata"
      />
    </div>
  );
};

export default AudioPlayer; 