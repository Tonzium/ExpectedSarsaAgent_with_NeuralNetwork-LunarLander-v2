import numpy as np
import json
with open("parameters.json", "r") as f:
    config = json.load(f)


class Adam():

    def __init__(self, layer_sizes):
        self.layer_sizes = layer_sizes

        # Specify Adam algorithm's hyper parameters
        self.step_size = config["optimizer_config"]["step_size"]
        self.beta_m = config["optimizer_config"]["beta_m"]
        self.beta_v = config["optimizer_config"]["beta_v"]
        self.epsilon = config["optimizer_config"]["epsilon"]
        
        # Initialize Adam algorithm's m and v
        self.m = [dict() for i in range(1, len(self.layer_sizes))]
        self.v = [dict() for i in range(1, len(self.layer_sizes))]
        
        for i in range(0, len(self.layer_sizes) - 1):
            
            # Momentum Weights
            self.m[i]["W"] = np.zeros((self.layer_sizes[i], self.layer_sizes[i+1]))
            # Momentum Bias
            self.m[i]["b"] = np.zeros((1, self.layer_sizes[i+1]))
            # Vector Weights
            self.v[i]["W"] = np.zeros((self.layer_sizes[i], self.layer_sizes[i+1]))
            # Vector Bias
            self.v[i]["b"] = np.zeros((1, self.layer_sizes[i+1]))
            
            
        # Notice that to calculate m_hat and v_hat, we use powers of beta_m and beta_v to 
        # the time step t. We can calculate these powers using an incremental product. At initialization then, 
        # beta_m_product and beta_v_product should be ...? (Note that timesteps start at 1 and if we were to 
        # start from 0, the denominator would be 0.)
        self.beta_m_product = self.beta_m
        self.beta_v_product = self.beta_v
    
    def update_weights(self, weights, td_errors_times_gradients):
        """
        Args:
            weights (Array of dictionaries): The weights of the neural network.
            td_errors_times_gradients (Array of dictionaries): The gradient of the 
            action-values with respect to the network's weights times the TD-error
        Returns:
            The updated weights (Array of dictionaries).
        """
        for i in range(len(weights)):
            for param in weights[i].keys():

                weight_update = None
        
                g = td_errors_times_gradients[i][param]
                self.m[i][param] = self.beta_m * self.m[i][param] + (1 - self.beta_m) * g
                self.v[i][param] = self.beta_v * self.v[i][param] + (1 - self.beta_v) * (g ** 2)

                m_hat = self.m[i][param] / (1 - self.beta_m_product)
                v_hat = self.v[i][param] / (1 - self.beta_v_product)

                weight_update = self.step_size * m_hat / (np.sqrt(v_hat) + self.epsilon)
                weights[i][param] = weights[i][param] + weight_update
        
        # Notice that to calculate m_hat and v_hat, we use powers of beta_m and beta_v to 
        ### update self.beta_m_product and self.beta_v_product
        self.beta_m_product *= self.beta_m
        self.beta_v_product *= self.beta_v
        
        return weights