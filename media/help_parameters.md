# Parameters Detailed Description 

## Power Spectrum Density Parameters 

`fmin` : Minimum frequency (Hz)

`fmax` : Maximum Frequency (Hz)

`tmin` : Low Boundary of the time Interval (s)

`tmax` : High Boundary of the time Interval (s)

##### Multitaper Method

`bandwidth` : Time-Bandwidth product. *A high Time-Bandwidth product enables more smoothing, and a better frequency precision.*

##### Welch Method


`n_fft` : Number of points used to compute the FFT. 

`n_per_seg` : Number of points in a segment.

`n_overlap` : Number of points of overlapping between two segments.

We typically aim for 3 to 6 segments with 50% of overlapping to have a good result. If the signal is N points, we would take N/2 points per segment, and an overlapping of N/4 points to have 3 segments total.
