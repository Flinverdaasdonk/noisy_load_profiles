import numpy as np
from typing import Dict, Any, Optional
from ..base import Perturbation


class ConstantRandomPercentualBias(Perturbation):
    """
    Applies multiplicative Gaussian noise to load profiles.
    
    The perturbation multiplies each profile by (1 + noise) where noise is
    sampled from a Gaussian distribution with specified mean and standard deviation.
    
    Formula: perturbed_profile = profile * (1 + gaussian_noise)
    """
    
    def __init__(self, uniform_low: float = -1, uniform_high: float = 1,
                 seed: Optional[int] = None, transformation: Optional[Dict[str, Any]] = None, 
                 track_input_profiles: bool = False):
        """
        Initialize the MultiplicativeGaussianNoise perturbation.
        
        Parameters:
        -----------
        uniform_low : float, default=-1
            Lower bound of the uniform distribution for bias
        uniform_high : float, default=1
            Upper bound of the uniform distribution for bias
        seed : int, optional
            Random seed for reproducibility
        transformation : Dict[str, Any], optional
            Pre-computed transformation parameters containing 'noise_samples'
        """
        super().__init__(seed=seed, transformation=transformation, track_input_profiles=track_input_profiles)
        
        self.uniform_low = uniform_low
        self.uniform_high = uniform_high
        
        # Store configuration
        self._config = {
            'uniform_low': uniform_low,
            'uniform_high': uniform_high
        }
        
        # Validate parameters
        if uniform_low >= uniform_high:
            raise ValueError(f"uniform_low ({uniform_low}) must be less than uniform_high ({uniform_high})")
    
    def _infer_transformation(self, profiles: np.ndarray) -> Dict[str, Any]:
        """
        Generate noise samples with the same shape as the input profiles.
        
        Parameters:
        -----------
        profiles : np.ndarray
            2D array where each column is a load profile, each row is a timestep
        """
        # Generate noise samples with same shape as profiles
        n_columns = profiles.shape[1]
        base_biases = np.random.uniform(low=self.uniform_low, high=self.uniform_high, size=(1, n_columns))

        abs_profiles = np.abs(profiles)
        # get the mean per column
        mean_profiles = np.mean(abs_profiles, axis=0, keepdims=True)
        # calculate the bias as a percentage of the mean
        biases = base_biases * mean_profiles 
        
        
        transformation = {
            'biases': biases,
            'shape': biases.shape,
            'uniform_low': self.uniform_low,
            'uniform_high': self.uniform_high}

        return transformation

    
    def _apply_perturbation(self, profiles: np.ndarray) -> np.ndarray:
        """
        Apply multiplicative Gaussian noise using stored transformation parameters.
        
        Parameters:
        -----------
        profiles : np.ndarray
            2D array where each column is a load profile, each row is a timestep
            
        Returns:
        --------
        np.ndarray
            The perturbed profiles: profiles * (1 + noise_samples)
        """
        
        # Add the biases to the profiles
        biases = self._transformation['biases']
        perturbed_profiles = profiles + biases

        
        return perturbed_profiles
    




class ConstantRandomPercentualScaling(Perturbation):
    """
    Applies multiplicative Gaussian noise to load profiles.
    
    The perturbation multiplies each profile by (1 + noise) where noise is
    sampled from a Gaussian distribution with specified mean and standard deviation.
    
    Formula: perturbed_profile = profile * (1 + gaussian_noise)
    """
    
    def __init__(self, uniform_low: float = 0.8, uniform_high: float = 1.2,
                 seed: Optional[int] = None, transformation: Optional[Dict[str, Any]] = None,
                 track_input_profiles: bool = False):
        """
        Initialize the MultiplicativeGaussianNoise perturbation.
        
        Parameters:
        -----------
        uniform_low : float, default=-1
            Lower bound of the uniform distribution for bias
        uniform_high : float, default=1
            Upper bound of the uniform distribution for bias
        seed : int, optional
            Random seed for reproducibility
        transformation : Dict[str, Any], optional
            Pre-computed transformation parameters containing 'noise_samples'
        """
        super().__init__(seed=seed, transformation=transformation, track_input_profiles=track_input_profiles)
        
        self.uniform_low = uniform_low
        self.uniform_high = uniform_high
        
        # Store configuration
        self._config = {
            'uniform_low': uniform_low,
            'uniform_high': uniform_high
        }
        
        # Validate parameters
        if uniform_low >= uniform_high:
            raise ValueError(f"uniform_low ({uniform_low}) must be less than uniform_high ({uniform_high})")
    
    def _infer_transformation(self, profiles: np.ndarray) -> Dict[str, Any]:
        """
        Generate noise samples with the same shape as the input profiles.
        
        Parameters:
        -----------
        profiles : np.ndarray
            2D array where each column is a load profile, each row is a timestep
        """
        # Generate noise samples with same shape as profiles
        n_columns = profiles.shape[1]
        base_scaling = np.random.uniform(low=self.uniform_low, high=self.uniform_high, size=(1, n_columns))
        
        transformation = {
            'scaling': base_scaling,
            'shape': biases.shape,
            'uniform_low': self.uniform_low,
            'uniform_high': self.uniform_high}

        return transformation

    
    def _apply_perturbation(self, profiles: np.ndarray) -> np.ndarray:
        """
        Apply multiplicative Gaussian noise using stored transformation parameters.
        
        Parameters:
        -----------
        profiles : np.ndarray
            2D array where each column is a load profile, each row is a timestep
            
        Returns:
        --------
        np.ndarray
            The perturbed profiles: profiles * (1 + noise_samples)
        """

        # Add the biases to the profiles
        scaling = self._transformation['scaling']

        perturbed_profiles = profiles * scaling

        
        return perturbed_profiles
    