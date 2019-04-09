//
//  ViewController.swift
//  TheSimpsonsClassifier
//
//  Created by A.Makarov on 05/04/2019.
//  Copyright © 2019 A.Makarov. All rights reserved.
//

import UIKit
import AVKit

class ViewController: UIViewController, UINavigationControllerDelegate {
    
    @IBOutlet weak var plotView: UIView!
    @IBOutlet weak var predictLabel: UILabel!
    @IBOutlet weak var plotImageView: UIImageView!
    
    var imagePicker: UIImagePickerController!
    var captureSession: AVCaptureSession!
    let predictionViewModel = PredictionViewModel()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        plotView.addShadowAndRadius(offset: CGSize(width: 3, height: 3), color: .gray, radius: 5, opacity: 0.5, cornerRadius: 10)
    }
    
    @IBAction func liveVideo(_ sender: Any) {
        plotImageView.image = nil
        
        // Add preview layer to our view to display the open camera screen
        if let session = captureSession {
            if session.isRunning { return }
            
            session.startRunning()
            let previewLayer = AVCaptureVideoPreviewLayer(session: session)
            previewLayer.name = "AVCapture"
            previewLayer.frame = plotView.bounds
            plotView.layer.addSublayer(previewLayer)
            return
        }
        
        //Start capture session
        captureSession = AVCaptureSession()
        captureSession.sessionPreset = .photo
        
        // Add input for capture
        guard let captureDevice = AVCaptureDevice.default(for: .video) else { return }
        guard let captureInput = try? AVCaptureDeviceInput(device: captureDevice) else { return }
        captureSession.addInput(captureInput)
        
        let previewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
        previewLayer.name = "AVCapture"
        previewLayer.frame = plotView.bounds
        plotView.layer.addSublayer(previewLayer)
        
        // Add output of capture
        let dataOutput = AVCaptureVideoDataOutput()
        dataOutput.videoSettings = [kCVPixelBufferPixelFormatTypeKey as String: Int(kCVPixelFormatType_32BGRA)]
        dataOutput.setSampleBufferDelegate(self, queue: DispatchQueue.global(qos: DispatchQoS.QoSClass.default))
        dataOutput.setSampleBufferDelegate(self, queue: DispatchQueue(label: "videoQueue"))
        captureSession.addOutput(dataOutput)
        
        captureSession.startRunning()
    }
    
    // MARK: - Take image or loading from library
    @IBAction func takePhoto(_ sender: UIButton) {
        
        if !UIImagePickerController.isSourceTypeAvailable(.camera) {
            print("Error. Camera not available")
            return
        }
        
        let cameraPicker = UIImagePickerController()
        cameraPicker.sourceType = .camera
        cameraPicker.delegate = self
        stopRunningVideo()
        present(cameraPicker, animated: true)
    }
    
    @IBAction func openLibrary(_ sender: Any) {
        let picker = UIImagePickerController()
        picker.sourceType = .photoLibrary
        picker.delegate = self
        stopRunningVideo()
        present(picker, animated: true)
    }
    
    func stopRunningVideo() {
        
        for layer in plotView.layer.sublayers! {
            if layer.name == "AVCapture" {
                layer.removeFromSuperlayer()
            }
        }
        captureSession?.stopRunning()
    }
}

extension ViewController: UIImagePickerControllerDelegate, AVCaptureVideoDataOutputSampleBufferDelegate {
    
    //MARK: - Image capture
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]){
        
        if let chosenImage = info[.originalImage] as? UIImage, let ciImage = CIImage(image: chosenImage) {
            plotImageView.image = chosenImage
            predictionViewModel.predictImage(.ciimage(img: ciImage)) { result in
                DispatchQueue.main.async { [weak self] in
                    self?.predictLabel.text = result
                }
            }
            
            picker.dismiss(animated: true, completion: nil)
        } else{
            print("Something went wrong")
        }
    }
    
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        dismiss(animated: true, completion: nil)
    }
    
    //MARK: - Video capture
    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {

        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else {
            return
        }
        
        predictionViewModel.predictImage(.pixels(buffer: pixelBuffer.resize(96))) { result in
            DispatchQueue.main.async { [weak self] in
                self?.predictLabel.text = result
            }
        }
    }
    
    func convert(cmage:CIImage) -> UIImage {
        let context:CIContext = CIContext.init(options: nil)
        let cgImage:CGImage = context.createCGImage(cmage, from: cmage.extent)!
        let image:UIImage = UIImage.init(cgImage: cgImage)
        return image
    }
}

