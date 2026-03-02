def get_spray_recommendation(insect_density_map, field_zones):
    """
    Generates spray recommendations based on insect density per zone.
    
    :param insect_density_map: A dict mapping zone_id to insect density (%).
    :param field_zones: A list of zone configurations.
    :return: A dict of recommendations per zone.
    """
    recommendations = {}
    
    # Example thresholds
    HIGH_DENSITY_THRESHOLD = 15.0  # 15%
    MEDIUM_DENSITY_THRESHOLD = 5.0 # 5%

    for zone in field_zones:
        zone_id = zone['id']
        density = insect_density_map.get(zone_id, 0)
        
        if density >= HIGH_DENSITY_THRESHOLD:
            action = "IMMEDIATE_SPRAY_REQUIRED"
            priority = "High"
            message = f"High insect density ({density:.2f}%) detected in Zone {zone_id}. Immediate spraying is recommended."
        elif density >= MEDIUM_DENSITY_THRESHOLD:
            action = "MONITOR_CLOSELY_OR_SPOT_SPRAY"
            priority = "Medium"
            message = f"Medium insect density ({density:.2f}%) detected in Zone {zone_id}. Consider spot spraying."
        else:
            action = "NO_ACTION_NEEDED"
            priority = "Low"
            message = f"Insect density ({density:.2f}%) in Zone {zone_id} is low. No action needed."
            
        recommendations[zone_id] = {
            "action": action,
            "priority": priority,
            "message": message,
            "density": density
        }
        
    return recommendations