//
//  UIVIewExtension.swift
//  TheSimpsonsClassifier
//
//  Created by A.Makarov on 05/04/2019.
//  Copyright © 2019 A.Makarov. All rights reserved.
//

import UIKit

extension UIView {
    
    func addShadowAndRadius(offset: CGSize, color: UIColor, radius: CGFloat, opacity: Float, cornerRadius: CGFloat) {
        layer.masksToBounds = false
        layer.shadowOffset = offset
        layer.shadowColor = color.cgColor
        layer.shadowRadius = radius
        layer.shadowOpacity = opacity
        layer.cornerRadius = radius
        
        let backgroundCGColor = backgroundColor?.cgColor
        backgroundColor = nil
        layer.backgroundColor =  backgroundCGColor
    }
}
