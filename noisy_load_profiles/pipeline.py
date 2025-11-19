import numpy as np
from typing import List, Dict, Any, Optional
import copy


class Pipeline:
    """
    Pipeline for applying multiple perturbations sequentially to load profiles.
    
    The pipeline applies perturbations in the order they are provided in the list.
    Each perturbation is applied to the result of the previous perturbation.
    """
    
    def __init__(self, perturbations: List['Perturbation'], seed: Optional[int] = None):
        """
        Initialize the pipeline with a list of perturbations.
        
        Parameters:
        -----------
        perturbations : List[Perturbation]
            List of perturbation objects to apply sequentially
        """
        if not perturbations:
            raise ValueError("Pipeline must contain at least one perturbation")
        
        self.perturbations = perturbations
        self._is_applied = False

        self.seed = seed
        if seed is not None:
            self.set_seed(seed)

    def apply(self, profiles: np.ndarray) -> np.ndarray:
        """
        Apply all perturbations sequentially to the input profiles.
        
        Parameters:
        -----------
        profiles : np.ndarray
            2D array where each column is a load profile, each row is a timestep
            
        Returns:
        --------
        np.ndarray
            Profiles after all perturbations have been applied
        """
        # Validate input
        self._validate_input(profiles)
        
        # Apply perturbations sequentially
        current_profiles = profiles.copy()
        
        for i, perturbation in enumerate(self.perturbations):
            try:
                current_profiles = perturbation.apply(current_profiles)
            except Exception as e:
                raise RuntimeError(f"Error applying perturbation {i} ({perturbation}): {repr(e)}")
        
        self._is_applied = True
        return current_profiles
    
    def track_perturbation_process(self, track: bool = True) -> None:
        """
        Enable or disable tracking of input profiles for each perturbation.
        
        Parameters:
        -----------
        track : bool, default=True
            If True, each perturbation will store the input profiles it receives
        """
        for perturbation in self.perturbations:
            perturbation.track_input_profiles = track

    def _validate_input(self, profiles: np.ndarray) -> None:
        """Validate that the input profiles are in the expected format."""
        if not isinstance(profiles, np.ndarray):
            raise TypeError("Profiles must be a numpy array")
        
        if profiles.ndim != 2:
            raise ValueError("Profiles must be a 2D array (timesteps x profiles)")
        
        if profiles.size == 0:
            raise ValueError("Profiles array cannot be empty")
    
    def get_transformations(self) -> List[Dict[str, Any]]:
        """
        Get the transformation parameters from all perturbations.
        
        Returns:
        --------
        List[Dict[str, Any]]
            List of transformation dictionaries, one for each perturbation
        """
        if not self._is_applied:
            return [None] * len(self.perturbations)
        
        return {p: p.get_transformation() for p in self.perturbations}
    
    def get_configs(self) -> List[Dict[str, Any]]:
        """
        Get the configuration parameters from all perturbations.
        
        Returns:
        --------
        List[Dict[str, Any]]
            List of configuration dictionaries, one for each perturbation
        """
        return {p: p.config for p in self.perturbations}
    
    def reset(self, increment_seed=True) -> None:
        """Reset all perturbations in the pipeline."""
        if increment_seed:

            if self.seed is not None:
                self.seed += 1
                self.set_seed(self.seed, reset=False)
            
            else:
                # get the current seeds and increment them by 1
                for perturbation in self.perturbations:
                    if perturbation.seed is not None:
                        perturbation.set_seed(perturbation.seed + 1, reset=False)

        for perturbation in self.perturbations:
            perturbation.reset()
            
        self._is_applied = False
        
    def set_seed(self, seed: int, reset=True) -> None:
        # set the seed for all perturbations
        if reset:
            self.reset()

        for perturbation in self.perturbations:
            perturbation.set_seed(seed)
    
    def __len__(self) -> int:
        """Return the number of perturbations in the pipeline."""
        return len(self.perturbations)
    
    def __getitem__(self, index: int) -> 'Perturbation':
        """Get a perturbation by index."""
        return self.perturbations[index]
    
    def __repr__(self) -> str:
        """String representation of the pipeline."""
        perturbation_names = ["\t" + repr(p) + "\n" for p in self.perturbations] 
        return f"Pipeline(\n" + "".join(perturbation_names) + ")"
    
    @property
    def config(self) -> Dict[str, Any]:
        """
        Get the configuration of the entire pipeline.
        
        Returns:
        --------
        Dict[str, Any]
            Dictionary containing pipeline configuration
        """
        return {
            'perturbations': self.get_configs(),
            'num_perturbations': len(self.perturbations)
        }


