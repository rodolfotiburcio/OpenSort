package OpenSort {
    private import ScalarValues::*;

    enum def StationExit {
        enum exit1;
        enum exit2;
        enum exit3;
        enum review;
    }

    item def PackageDetected;
    item def QrResult {
        doc /* Una lectura válida entrega el ID del paquete. Un fallo de
               lectura o un timeout se trata como QR ilegible. */
        attribute readable : Boolean;
        attribute packageId : String [0..1];
    }
    item def DestinationQuery {
        attribute packageId : String;
    }
    enum def LookupStatus {
        enum found;
        enum unknownId;
        enum unavailable;
    }
    item def DestinationResult {
        attribute status : LookupStatus;
        attribute destination : String [0..1];
    }
    item def DivertOrder {
        attribute expectedExit : StationExit;
    }
    item def ExitObservation {
        attribute observedExit : StationExit;
    }

    port def EntrySignal { out item detected : PackageDetected; }
    port def QrSignal { out item result : QrResult; }
    port def ManifestAccess {
        out item query : DestinationQuery;
        in item result : DestinationResult;
    }
    port def DivertSignal { out item order : DivertOrder; }
    port def ExitSignal { out item observation : ExitObservation; }

    part def BenchStation {
        doc /* V1 admite un paquete por ciclo. Las conexiones representan
               intercambios lógicos. Quedan por definir pines, polaridad,
               filtrado, protocolo del lector, mando del desviador, ubicación
               del manifiesto y tiempos de lectura, posicionamiento y salida. */
        part entrySensor { port signal : EntrySignal; }
        part qrReader { port signal : QrSignal; }
        part manifestSource { port access : ~ManifestAccess; }
        part diverter { port signal : ~DivertSignal; }
        part exitSensors {
            doc /* Agrupa los sensores de las tres salidas y de revisión. */
            port signal : ExitSignal;
        }
        part controller {
            doc /* Controlador previsto: ESP32. */
            port entry : ~EntrySignal;
            port qr : ~QrSignal;
            port manifest : ManifestAccess;
            port divert : DivertSignal;
            port exitObservation : ~ExitSignal;
        }

        connect entrySensor.signal to controller.entry;
        connect qrReader.signal to controller.qr;
        connect controller.manifest to manifestSource.access;
        connect controller.divert to diverter.signal;
        connect exitSensors.signal to controller.exitObservation;
    }

    action def PackageCycle {
        doc /* Flujo funcional de un intento. Los valores de decisión resumen
               los resultados de lectura, consulta y confirmación. La estación
               abre el ciclo al activarse el sensor de entrada estando libre. */
        in qrReadable : Boolean;
        in manifestAvailable : Boolean;
        in routeFound : Boolean;
        in exitMatches : Boolean;

        first start;
        then action detectPackage;
        then action readQr;
        then decide qrDecision;
            if qrReadable then queryManifest;
            else selectReview;

        action queryManifest;
        then decide manifestDecision;
            if manifestAvailable then checkRoute;
            else pendingManifestFailurePolicy;

        action checkRoute {
            doc /* Se requiere un ID conocido y una ruta para su destino. */
        }
        then decide routeDecision;
            if routeFound then selectDestinationExit;
            else selectReview;

        action selectDestinationExit;
        then selectedExit;
        action selectReview;
        then selectedExit;

        merge selectedExit;
        then action orderDiversion;
        then action awaitExit {
            doc /* La observación es independiente de la orden. El resultado
                   exitMatches es falso si se observa otra salida o vence el
                   plazo sin observación. También se confirma la salida de revisión. */
        }
        then decide exitDecision;
            if exitMatches then recordConfirmedExit;
            else blockAdmission;

        action recordConfirmedExit;
        then done;

        action blockAdmission {
            doc /* Registra la discrepancia o el timeout y bloquea la
                   admisión del siguiente paquete. Rearme por definir. */
        }
        then done;

        action pendingManifestFailurePolicy {
            doc /* Caso abierto. Termina aquí el flujo documentado para esta
                   rama. La respuesta operativa de la estación sigue por definir. */
        }
        then done;
    }
}
