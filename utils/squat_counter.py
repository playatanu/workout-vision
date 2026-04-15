class SquatCounter:
    def __init__(self):
        self.count = 0
        self.stage = "UP"
        
    def get_right_leg_points(self, keypoints, w, h):
        hip = keypoints[0][0][12]
        knee = keypoints[0][0][14]
        ankle = keypoints[0][0][16]


        return (
            (hip[1]*w, hip[0]*h),
            (knee[1]*w, knee[0]*h),
            (ankle[1]*w, ankle[0]*h),
            hip[2], knee[2], ankle[2]
        )
    

    def update(self, angle):
        # Down position
        if angle < 100:
            self.stage = "DOWN"

        # Up position (count rep)
        if angle > 160 and self.stage == "DOWN":
            self.stage = "UP"
            self.count += 1

        return self.count, self.stage