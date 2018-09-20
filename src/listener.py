import pyaudio
import numpy
import wave

class Listener():
  default_chunksize = 8192
  default_format = pyaudio.paInt16
  default_channels = 2
  default_rate = 44100
  default_seconds = 0

  def __init__(self):
    self.audio = pyaudio.PyAudio()
    self.stream = None
    self.data = []
    self.channels = Listener.default_channels
    self.chunksize = Listener.default_chunksize
    self.rate = Listener.default_rate
    self.recorded = False

  def start_recording(self, channels=default_channels,
                      rate=default_rate,
                      chunksize=default_chunksize,
                      seconds=default_seconds):
    self.chunksize = chunksize
    self.channels = channels
    self.recorded = False
    self.rate = rate

    if self.stream:
      self.stream.stop_stream()
      self.stream.close()

    self.stream = self.audio.open(
      format=self.default_format,
      channels=channels,
      rate=rate,
      input=True,
      frames_per_buffer=chunksize,
    )
    self.data = [[] for i in range(channels)]


  def process_recording(self):
    data = self.stream.read(self.chunksize)
    nums = numpy.fromstring(data, numpy.int16)
   
    for c in range(self.channels):
      self.data[c].extend(nums[c::self.channels])
    
    return nums

  def stop_recording(self):
    self.stream.stop_stream()
    self.stream.close()
    self.stream = None
    self.recorded = True

  def get_recorded_data(self):
    return self.data

  def save_recorded(self, output_filename):
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(self.channels)
    wf.setsampwidth(self.audio.get_sample_size(self.default_format))
    wf.setframerate(self.rate)

    chunk_length = len(self.data[0]) / self.channels
    result = numpy.reshape(self.data[0], (chunk_length, self.channels))
    wf.writeframes(result)
    wf.close()

  def play(self):
    pass

  def get_recorded_time(self):
    return len(self.data[0]) / self.rate
