# -*- coding: utf-8 -*-
"""
Geometry module - Point, Line, and coordinate transformation utilities.

Contains classes for handling both Cartesian and triangular (ternary) coordinates,
with conversion utilities between coordinate systems.
"""

import numpy as np


class Tool:
    """
    Utility class providing coordinate transformation and geometric calculations.
    
    Methods include:
    - Triangular to binary coordinate conversion
    - Binary to triangular coordinate conversion
    - Line intersection calculations
    - Region filling helpers
    """

    def TriToBin(self, x, y, z):
        """
        Convert triangular (ternary) coordinates to binary (Cartesian) coordinates.
        
        Args:
            x, y, z: The three components of the triangular coordinate
            
        Returns:
            tuple: (a, b) binary coordinates
        """
        if z >= 0:
            if x + y + z == 0:
                return (0, 0)
            Sum = x + y + z
            X = 100.0 * x / Sum
            Y = 100.0 * y / Sum
            Z = 100.0 * z / Sum
            if X + Y != 0:
                a = Z / 2.0 + (100.0 - Z) * Y / (Y + X)
            else:
                a = Z / 2.0
            b = Z / 2.0 * np.sqrt(3)
            return (a, b)
        else:
            z = abs(z)
            if x + y + z == 0:
                return (0, 0)
            Sum = x + y + z
            X = 100.0 * x / Sum
            Y = 100.0 * y / Sum
            Z = 100.0 * z / Sum
            if X + Y != 0:
                a = Z / 2.0 + (100.0 - Z) * Y / (Y + X)
            else:
                a = Z / 2.0
            b = Z / 2.0 * np.sqrt(3)
            return (a, -b)

    def BinToTri(self, a, b):
        """
        Convert binary (Cartesian) coordinates to triangular (ternary) coordinates.
        
        Args:
            a, b: Binary coordinates
            
        Returns:
            tuple: (x, y, z) triangular coordinates
        """
        if b >= 0:
            y = a - b / np.sqrt(3)
            z = b * 2 / np.sqrt(3)
            x = 100 - (a + b / np.sqrt(3))
            return (x, y, z)
        else:
            y = a + b / np.sqrt(3)
            z = b * 2 / np.sqrt(3)
            x = 100 - (a - b / np.sqrt(3))
            return (x, y, z)

    def Cross(self, A=[(0, 0), (10, 10)], B=[(0, 10), (100, 0)]):
        """
        Calculate the intersection point of two lines in Cartesian coordinates.
        
        Args:
            A: First line as [(x0,y0), (x1,y1)]
            B: Second line as [(x2,y2), (x3,y3)]
            
        Returns:
            list: [x, y] intersection coordinates
        """
        x0, y0 = A[0]
        x1, y1 = A[1]
        x2, y2 = B[0]
        x3, y3 = B[1]

        # Handle vertical lines
        if x1 - x0 == 0:
            b1 = 1e9
        else:
            b1 = (y1 - y0) / (x1 - x0)
        
        if x3 - x2 == 0:
            b2 = 1e9
        else:
            b2 = (y3 - y2) / (x3 - x2)

        c1 = y0 - b1 * x0
        c2 = y2 - b2 * x2

        if b1 - b2 == 0:
            x = 0
        else:
            x = (c2 - c1) / (b1 - b2)
        y = b1 * x + c1

        return [x, y]

    def TriCross(self, A=[(100, 0, 0), (0, 50, 60)], B=[(50, 50, 0), (0, 0, 100)]):
        """
        Calculate intersection of two lines in triangular coordinates.
        
        Args:
            A: First line as [(x0,y0,z0), (x1,y1,z1)]
            B: Second line as [(x2,y2,z2), (x3,y3,z3)]
            
        Returns:
            tuple: (x, y, z) intersection in triangular coordinates
        """
        x0, y0 = self.TriToBin(A[0][0], A[0][1], A[0][2])
        x1, y1 = self.TriToBin(A[1][0], A[1][1], A[1][2])
        x2, y2 = self.TriToBin(B[0][0], B[0][1], B[0][2])
        x3, y3 = self.TriToBin(B[1][0], B[1][1], B[1][2])

        if x1 - x0 == 0:
            b1 = 1e9
        else:
            b1 = (y1 - y0) / (x1 - x0)
        
        if x3 - x2 == 0:
            b2 = 1e9
        else:
            b2 = (y3 - y2) / (x3 - x2)

        c1 = y0 - b1 * x0
        c2 = y2 - b2 * x2

        if b1 - b2 == 0:
            x = 0
        else:
            x = (c2 - c1) / (b1 - b2)
        y = b1 * x + c1

        return self.BinToTri(x, y)

    def Fill(self, P=[(100, 0), (85, 15), (0, 3)], Color='blue', Alpha=0.3):
        """
        Extract x and y lists from polygon vertices for filling.
        
        Args:
            P: List of (x, y) tuples defining polygon vertices
            Color: Fill color (unused, kept for compatibility)
            Alpha: Fill transparency (unused, kept for compatibility)
            
        Returns:
            tuple: (x_list, y_list) for polygon filling
        """
        a = [p[0] for p in P]
        b = [p[1] for p in P]
        return (a, b)

    def TriFill(self, P=[(100, 0, 0), (85, 15, 0), (0, 3, 97)], Color='blue', Alpha=0.3):
        """
        Convert triangular polygon vertices to binary coordinates for filling.
        
        Args:
            P: List of (x, y, z) tuples in triangular coordinates
            Color: Fill color (unused, kept for compatibility)
            Alpha: Fill transparency (unused, kept for compatibility)
            
        Returns:
            tuple: (x_list, y_list) in binary coordinates for filling
        """
        a = [self.TriToBin(p[0], p[1], p[2])[0] for p in P]
        b = [self.TriToBin(p[0], p[1], p[2])[1] for p in P]
        return (a, b)

    def LogRatioTriToBin(self, x, y, z):
        """
        Convert triangular coordinates to log-ratio binary coordinates.
        
        Args:
            x, y, z: Triangular coordinates (must all be positive)
            
        Returns:
            tuple: (V, W) log-ratio coordinates, or None if invalid
        """
        if x > 0 and y > 0 and z > 0:
            Sum = x + y + z
            X = 100.0 * x / Sum
            Y = 100.0 * y / Sum
            Z = 100.0 * z / Sum
            V = np.log(X / Z)
            W = np.log(Y / Z)
            return (V, W)
        return None

    def BackLogRatioBinToTri(self, V, W):
        """
        Convert log-ratio coordinates back to triangular coordinates.
        
        Args:
            V, W: Log-ratio coordinates
            
        Returns:
            tuple: (X, Y, Z) triangular coordinates
        """
        a = np.power(np.e, V)
        b = np.power(np.e, W)
        X = a / (a + b + 1)
        Y = b / (a + b + 1)
        Z = 1 / (a + b + 1)
        return (X, Y, Z)


class Point:
    """
    A point class for Cartesian coordinates with styling attributes.
    
    Attributes:
        X, Y: Coordinate values
        Location: (X, Y) tuple
        Size: Marker size for plotting
        Color: Marker color
        Alpha: Transparency (0-1)
        Marker: Marker style ('o', 'd', '*', '^', etc.)
        Label: Text label for the point
    """

    def __init__(self, X=0, Y=0, Size=12, Color='red', Alpha=0.3, Marker='o', Label=''):
        self.X = X
        self.Y = Y
        self.Location = (X, Y)
        self.Size = Size
        self.Color = Color
        self.Alpha = Alpha
        self.Marker = Marker
        self.Label = Label


class Points:
    """
    A class for handling multiple points with uniform styling.
    
    Attributes:
        X, Y: Lists of coordinate values
        Size: Marker size for all points
        Color: Marker color for all points
        Alpha: Transparency for all points
        Marker: Marker style for all points
        Label: Shared label
        FontSize: Font size for labels
    """

    def __init__(self, points=[(0, 0), (0, 1)], Size=12, Color='red', Alpha=0.3, 
                 Marker='o', Label='', FontSize=8):
        self.X = [p[0] for p in points]
        self.Y = [p[1] for p in points]
        self.Size = Size
        self.Color = Color
        self.Alpha = Alpha
        self.Marker = Marker
        self.Label = Label
        self.FontSize = FontSize


class Tag:
    """
    A text tag/label class for annotations.
    
    Attributes:
        Label: The text content
        Location: (x, y) position
        X_offset, Y_offset: Offset from location
        FontSize: Text size
    """

    def __init__(self, Label='Label', Location=(0, 0), X_offset=-6, Y_offset=3, FontSize=8):
        self.Label = Label
        self.Location = Location
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.FontSize = FontSize


class Line:
    """
    A line class connecting multiple points with styling.
    
    Attributes:
        Points: List of (x, y) coordinate tuples
        X, Y: Extracted x and y coordinate lists
        Width: Line width
        Color: Line color
        Style: Line style ('-', '--', '-.', ':')
        Alpha: Transparency
        Label: Line label
        Sort: Sorting option ('x', 'y', or '' for no sort)
    """

    def __init__(self, Points=[(0, 0), (1, 1)], Sort='', Width=1, Color='blue', 
                 Style='-', Alpha=0.3, Label=''):
        self.Sort = Sort
        self.Width = Width
        self.Color = Color
        self.Style = Style
        self.Alpha = Alpha
        self.Label = Label
        self.Points = Points

        if len(Points) >= 2:
            self.X = [p[0] for p in Points]
            self.Y = [p[1] for p in Points]
        else:
            self.X = []
            self.Y = []

    def sequence(self):
        """Sort points according to the Sort attribute."""
        if len(self.Points) > 0 and len(self.Points[0]) >= 2:
            if self.Sort.lower() == 'x':
                self.Points.sort(key=lambda p: p[0])
            elif self.Sort.lower() == 'y':
                self.Points.sort(key=lambda p: p[1])
            elif self.Sort.lower() == 'z' and len(self.Points[0]) >= 3:
                self.Points.sort(key=lambda p: p[2])
            self._update_xy()

    def _update_xy(self):
        """Update X and Y lists from Points."""
        self.X = [p[0] for p in self.Points]
        self.Y = [p[1] for p in self.Points]


class TriTag(Tag, Tool):
    """
    A text tag for triangular coordinate systems.
    
    Inherits from Tag and Tool to provide coordinate conversion.
    """

    def __init__(self, Label='Label', Location=(0, 1, 2), X_offset=-6, Y_offset=3, FontSize=12):
        self.Label = Label
        self.Location = self.TriToBin(Location[0], Location[1], Location[2])
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.FontSize = FontSize


class TriPoint(Point, Tool):
    """
    A point class for triangular coordinate systems.
    
    Inherits from Point and Tool to provide coordinate conversion.
    Stores both triangular (x, y, z) and binary (X, Y) coordinates.
    """

    def __init__(self, P=(10, 20, 70), Size=12, Color='red', Alpha=0.3, Marker='o', Label=''):
        Point.__init__(self, Size=Size, Color=Color, Alpha=Alpha, Marker=Marker, Label=Label)
        
        self.sum = P[0] + P[1] + abs(P[2])
        if self.sum == 0:
            self.sum = 1
        
        self.x = P[0] * 100 / self.sum
        self.y = P[1] * 100 / self.sum
        self.z = P[2] * 100 / self.sum
        
        # Log-ratio coordinates
        if self.x > 0 and self.z > 0:
            self.V = np.log(self.x / self.z)
            self.W = np.log(self.y / self.z) if self.y > 0 else 0
        else:
            self.V = 0
            self.W = 0

        self.Location = P
        self.X, self.Y = self.TriToBin(self.x, self.y, self.z)


class TriLine(Line, Tool):
    """
    A line class for triangular coordinate systems.
    
    Inherits from Line and Tool to provide coordinate conversion.
    Stores both triangular (x, y, z) and binary (X, Y) coordinates.
    """

    def __init__(self, Points=[(0, 0, 0), (1, 1, 1)], Sort='', Width=1, Color='blue', 
                 Style='-', Alpha=0.3, Label=''):
        self.Sort = Sort
        self.Width = Width
        self.Color = Color
        self.Style = Style
        self.Alpha = Alpha
        self.Label = Label
        self.Points = Points

        self.x = [p[0] for p in Points]
        self.y = [p[1] for p in Points]
        self.z = [p[2] for p in Points]

        self.sequence()
        self._tritrans()

    def _tritrans(self):
        """Convert triangular coordinates to binary coordinates."""
        self.X = []
        self.Y = []
        for i in range(len(self.x)):
            bin_coords = self.TriToBin(self.x[i], self.y[i], self.z[i])
            self.X.append(bin_coords[0])
            self.Y.append(bin_coords[1])

    def sequence(self):
        """Sort points and update coordinate lists."""
        if len(self.Points) > 0:
            if self.Sort.lower() == 'x':
                self.Points.sort(key=lambda p: p[0])
            elif self.Sort.lower() == 'y':
                self.Points.sort(key=lambda p: p[1])
            elif self.Sort.lower() == 'z':
                self.Points.sort(key=lambda p: p[2])
            
            self.x = [p[0] for p in self.Points]
            self.y = [p[1] for p in self.Points]
            self.z = [p[2] for p in self.Points]
