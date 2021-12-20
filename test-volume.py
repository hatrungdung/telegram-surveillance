import numpy as np
import sounddevice as sd
from pydub import AudioSegment

seconds = 5
SAMPLE_RATE = 44100


def _record_buffer(buffer, **kwargs):
    """Record from microphone to buffer

    Args:
        buffer (bytes): A bytes buffer to record to.

    Raises:
        sd.CallbackStop: callback(indata, frame_count, time_info, status).

    Returns:
        stream (sounddevice.InputStream): Stream as a file type object.
        event (Event): event.is_set() will be True once audio has finished recording.
    """
    class Event:
        """Class to mark an event.
        """
        _set = False

        def set(self):
            """Signals event completion.
            """
            self._set = True

        def is_set(self):
            """Test whether event has completed.

            Returns:
                Boolean: True if event has completed.
            """
            return self._set

    event = Event()
    idx = 0

    def callback(indata, frame_count, time_info, status):  # pylint: disable=unused-argument
        nonlocal idx
        remainder = len(buffer) - idx
        if remainder == 0:
            event.set()
            raise sd.CallbackStop
        indata = indata[:remainder]
        buffer[idx:idx + len(indata)] = indata
        idx += len(indata)

    stream = sd.InputStream(callback=callback,
                            dtype=buffer.dtype,
                            channels=buffer.shape[1],
                            **kwargs)
    return stream, event

while True:
    buffer = np.empty((int(seconds * SAMPLE_RATE), 1), dtype=np.int32)
    stream, event = _record_buffer(buffer, samplerate=SAMPLE_RATE)
    with stream:
        while not event.is_set():
            sd.sleep(10)
    print(np.linalg.norm(buffer) / pow(2, 31))