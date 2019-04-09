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

extension CVPixelBuffer {
    
    func resize(_ size: Int) -> CVPixelBuffer {
        let imageSide = size
        var ciImage = CIImage(cvPixelBuffer: self, options: nil)
        let transform = CGAffineTransform(scaleX: CGFloat(imageSide) / CGFloat(CVPixelBufferGetWidth(self)), y: CGFloat(imageSide) / CGFloat(CVPixelBufferGetHeight(self)))
        ciImage = ciImage.transformed(by: transform).cropped(to: CGRect(x: 0, y: 0, width: imageSide, height: imageSide))
        let ciContext = CIContext()
        var resizeBuffer: CVPixelBuffer?
        CVPixelBufferCreate(kCFAllocatorDefault, imageSide, imageSide, CVPixelBufferGetPixelFormatType(self), nil, &resizeBuffer)
        ciContext.render(ciImage, to: resizeBuffer!)
        return resizeBuffer!
    }
}
